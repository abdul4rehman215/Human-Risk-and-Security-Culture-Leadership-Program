#!/usr/bin/env python3
"""
Filter and display high-risk roles
"""

import json


def filter_high_risk_roles(report_file, threshold=60):
    """
    Filter roles with risk score above threshold.

    Args:
        report_file: Path to risk report JSON
        threshold: Minimum risk score to include
    """
    # Load the risk report
    try:
        with open(report_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Report file not found: {report_file}")
        return
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in report file")
        return

    detailed = data.get("detailed_analysis", {})

    # Filter roles with final_score >= threshold
    filtered = []
    for role_id, info in detailed.items():
        try:
            score = float(info.get("final_score", 0))
        except (TypeError, ValueError):
            continue

        if score >= threshold:
            filtered.append((role_id, info))

    # Sort by score (descending)
    filtered.sort(key=lambda x: float(x[1].get("final_score", 0)), reverse=True)

    # Print formatted results
    print(f"\nHigh-Risk Roles (final_score >= {threshold})")
    print("=" * 70)
    print(f"{'Rank':<6}{'Role Name':<30}{'Department':<20}{'Score':<8}{'Level':<10}")
    print("-" * 70)

    for idx, (role_id, info) in enumerate(filtered, start=1):
        print(
            f"{idx:<6}"
            f"{info.get('role_name', 'Unknown'):<30}"
            f"{info.get('department', 'Unknown'):<20}"
            f"{float(info.get('final_score', 0)):<8.2f}"
            f"{info.get('risk_level', 'Unknown'):<10}"
        )

    print("-" * 70)
    print(f"Total high-risk roles found: {len(filtered)}\n")


if __name__ == "__main__":
    filter_high_risk_roles("comprehensive_risk_report.json", 60)
