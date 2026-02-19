#!/usr/bin/env python3
import csv
import json
from datetime import datetime
from typing import List, Dict, Any


def process_malware_hashes(input_file: str) -> List[Dict[str, Any]]:
    """
    Process malware hash indicators from MalwareBazaar.

    Args:
        input_file: Path to CSV file with malware hashes

    Returns:
        List of processed indicator dictionaries
    """
    processed = []
    count = 0

    # Open and read the CSV file
    # Skip comment lines starting with '#'
    # Extract relevant fields: timestamp, hash, malware_family
    # Add threat_level='High', source='MalwareBazaar', type='File Hash'
    # Limit to first 50 records
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # MalwareBazaar export is CSV-like; we parse using csv.reader for robustness
                row = next(csv.reader([line]))
                # Common columns for bazaar export can vary; we try best-effort extraction:
                # timestamp is often at index 0, sha256 at index 1, malware family sometimes later.
                timestamp = row[0] if len(row) > 0 else ""
                sha256_hash = row[1] if len(row) > 1 else ""
                malware_family = row[2] if len(row) > 2 else ""

                if not sha256_hash:
                    continue

                record = {
                    "timestamp": timestamp,
                    "indicator_value": sha256_hash,
                    "malware_family": malware_family,
                    "threat_level": "High",
                    "source": "MalwareBazaar",
                    "type": "File Hash",
                    "description": f"Malware family: {malware_family}" if malware_family else "Malware hash indicator",
                }
                processed.append(record)
                count += 1
                if count >= 50:
                    break
    except FileNotFoundError:
        print(f"[ERROR] Malware hashes file not found: {input_file}")
    except Exception as e:
        print(f"[ERROR] Failed processing malware hashes: {e}")

    return processed


def process_ip_indicators(input_file: str) -> List[Dict[str, Any]]:
    """
    Process IP reputation data from Feodo Tracker.

    Args:
        input_file: Path to file with malicious IPs

    Returns:
        List of processed IP indicator dictionaries
    """
    processed = []
    count = 0

    # Read file line by line
    # Skip comments and empty lines
    # Extract IP addresses
    # Create records with: ip_address, threat_level='Medium',
    # source='Feodo Tracker', type='IP Address'
    # Limit to first 50 records
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Feodo IP blocklist CSV lines usually start with IP
                # We take first CSV field as IP address
                row = next(csv.reader([line]))
                ip_address = row[0].strip() if row else ""
                if not ip_address:
                    continue

                record = {
                    "timestamp": "",  # may not be present in this feed
                    "indicator_value": ip_address,
                    "threat_level": "Medium",
                    "source": "Feodo Tracker",
                    "type": "IP Address",
                    "description": "Known malicious/botnet C2 IP (Feodo Tracker)",
                }
                processed.append(record)
                count += 1
                if count >= 50:
                    break
    except FileNotFoundError:
        print(f"[ERROR] Feodo IP file not found: {input_file}")
    except Exception as e:
        print(f"[ERROR] Failed processing IP indicators: {e}")

    return processed


def process_url_indicators(input_file: str) -> List[Dict[str, Any]]:
    """
    Process malicious URL indicators from URLhaus.

    Args:
        input_file: Path to CSV with malicious URLs

    Returns:
        List of processed URL indicator dictionaries
    """
    processed = []
    count = 0

    # Open and parse CSV file
    # Skip comment lines
    # Extract: timestamp, url, status
    # Add threat_level='High', source='URLhaus', type='URL/Domain'
    # Limit to first 50 records
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                row = next(csv.reader([line]))
                # URLhaus CSV often has: id, dateadded, url, url_status, ...
                # We'll best-effort map:
                timestamp = ""
                url = ""
                status = ""

                if len(row) >= 4:
                    timestamp = row[1]
                    url = row[2]
                    status = row[3]
                elif len(row) >= 3:
                    timestamp = row[0]
                    url = row[1]
                    status = row[2]
                elif len(row) >= 2:
                    url = row[0]
                    status = row[1]
                else:
                    continue

                if not url:
                    continue

                record = {
                    "timestamp": timestamp,
                    "indicator_value": url,
                    "status": status,
                    "threat_level": "High",
                    "source": "URLhaus",
                    "type": "URL/Domain",
                    "description": f"URLhaus malicious URL (status: {status})" if status else "URLhaus malicious URL",
                }
                processed.append(record)
                count += 1
                if count >= 50:
                    break
    except FileNotFoundError:
        print(f"[ERROR] URLhaus file not found: {input_file}")
    except Exception as e:
        print(f"[ERROR] Failed processing URL indicators: {e}")

    return processed


def create_master_dataset() -> List[Dict[str, Any]]:
    """Combine all CTI sources into master dataset."""
    all_indicators: List[Dict[str, Any]] = []

    malware = process_malware_hashes("data/malware_hashes.csv")
    ips = process_ip_indicators("data/feodo_ips.csv")
    urls = process_url_indicators("data/urlhaus_domains.csv")

    all_indicators.extend(malware)
    all_indicators.extend(ips)
    all_indicators.extend(urls)

    # Save as JSON to output/master_cti_dataset.json
    with open("output/master_cti_dataset.json", "w", encoding="utf-8") as f:
        json.dump(all_indicators, f, indent=2)

    # Save as CSV to output/master_cti_dataset.csv
    csv_headers = ["timestamp", "type", "indicator_value", "threat_level", "source", "description"]
    with open("output/master_cti_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for rec in all_indicators:
            writer.writerow({
                "timestamp": rec.get("timestamp", ""),
                "type": rec.get("type", ""),
                "indicator_value": rec.get("indicator_value", ""),
                "threat_level": rec.get("threat_level", ""),
                "source": rec.get("source", ""),
                "description": rec.get("description", ""),
            })

    print(f"Processed {len(all_indicators)} indicators")
    return all_indicators


if __name__ == "__main__":
    create_master_dataset()
