#!/usr/bin/env python3
import csv
import json
from collections import defaultdict
from typing import Dict, Any, List


def calculate_risk_score(record: Dict[str, Any]) -> int:
    """
    Calculate numerical risk score (1-10) for an indicator.

    Scoring factors:
    - Threat level: High=7, Medium=4, Low=1
    - Source reliability: +2 for trusted sources
    - Indicator type: URL/Domain=+3, IP=+2, Hash=+1

    Args:
        record: Dictionary with indicator data

    Returns:
        Integer risk score (1-10)
    """
    score = 0

    # Implement scoring logic based on threat_level
    threat_level = (record.get("threat_level") or "").strip().lower()
    if threat_level == "high":
        score += 7
    elif threat_level == "medium":
        score += 4
    elif threat_level == "low":
        score += 1
    else:
        score += 2  # unknown baseline

    # Add points for source reliability
    trusted_sources = {"malwarebazaar", "feodo tracker", "urlhaus"}
    source = (record.get("source") or "").strip().lower()
    if source in trusted_sources:
        score += 2

    # Add points for indicator type
    itype = (record.get("type") or "").strip().lower()
    if "url" in itype or "domain" in itype:
        score += 3
    elif "ip" in itype:
        score += 2
    elif "hash" in itype:
        score += 1

    # Cap maximum score at 10
    if score > 10:
        score = 10
    if score < 1:
        score = 1

    return score


def load_master_data() -> List[Dict[str, Any]]:
    with open("output/master_cti_dataset.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_main_sheet(data: List[Dict[str, Any]]) -> None:
    """
    Create main CTI indicators spreadsheet.

    Columns: ID, Timestamp, Type, Indicator_Value, Threat_Level,
    Source, Description, Risk_Score
    """
    headers = [
        "ID",
        "Timestamp",
        "Type",
        "Indicator_Value",
        "Threat_Level",
        "Source",
        "Description",
        "Risk_Score",
    ]

    with open("output/cti_main_sheet.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for idx, rec in enumerate(data, start=1):
            indicator_value = rec.get("indicator_value", "")
            risk_score = calculate_risk_score(rec)

            writer.writerow([
                idx,
                rec.get("timestamp", ""),
                rec.get("type", ""),
                indicator_value,
                rec.get("threat_level", ""),
                rec.get("source", ""),
                rec.get("description", ""),
                risk_score,
            ])


def create_risk_summary(data: List[Dict[str, Any]]) -> None:
    """
    Create risk assessment summary sheet.

    Columns: Threat_Category, Count, High_Risk, Medium_Risk,
    Low_Risk, Priority_Score
    """
    # Group indicators by type and count threat levels
    summary = defaultdict(lambda: {"Count": 0, "High": 0, "Medium": 0, "Low": 0, "Priority_Score": 0})

    for rec in data:
        category = rec.get("type", "Unknown")
        tl = (rec.get("threat_level") or "").strip().lower()

        summary[category]["Count"] += 1
        if tl == "high":
            summary[category]["High"] += 1
        elif tl == "medium":
            summary[category]["Medium"] += 1
        elif tl == "low":
            summary[category]["Low"] += 1

        summary[category]["Priority_Score"] += calculate_risk_score(rec)

    headers = ["Threat_Category", "Count", "High_Risk", "Medium_Risk", "Low_Risk", "Priority_Score"]

    with open("output/cti_risk_summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for cat, stats in summary.items():
            writer.writerow([
                cat,
                stats["Count"],
                stats["High"],
                stats["Medium"],
                stats["Low"],
                stats["Priority_Score"],
            ])


if __name__ == "__main__":
    data = load_master_data()
    create_main_sheet(data)
    create_risk_summary(data)
    print("Spreadsheets created: output/cti_main_sheet.csv and output/cti_risk_summary.csv")
