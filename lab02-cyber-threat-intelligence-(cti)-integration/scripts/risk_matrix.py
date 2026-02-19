#!/usr/bin/env python3
import json
import csv
from collections import defaultdict
from statistics import mean


def create_risk_matrix():
    """
    Create risk prioritization matrix CSV.

    Categories:
    - Critical (12-15): Immediate response required
    - High (8-11): Urgent investigation needed
    - Medium (5-7): Scheduled review
    - Low (1-4): Routine monitoring
    """
    # Load risk assessment report
    with open("output/risk_assessment_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    threats = report.get("top_10_prioritized_threats", [])
    # NOTE: Top 10 only included in report. For full dataset prioritization matrix,
    # re-run scoring on master dataset. But lab asked from report; keeping as-is.

    categories = {
        "Critical (12-15)": [],
        "High (8-11)": [],
        "Medium (5-7)": [],
        "Low (1-4)": []
    }

    for t in threats:
        score = int(t.get("priority_score", 0))
        if 12 <= score <= 15:
            categories["Critical (12-15)"].append(t)
        elif 8 <= score <= 11:
            categories["High (8-11)"].append(t)
        elif 5 <= score <= 7:
            categories["Medium (5-7)"].append(t)
        else:
            categories["Low (1-4)"].append(t)

    # Calculate statistics for each category
    # Create CSV with columns: Risk_Category, Count,
    # Indicator_Types, Avg_Score, Primary_Action, Timeline
    output_file = "output/risk_matrix.csv"
    headers = ["Risk_Category", "Count", "Indicator_Types", "Avg_Score", "Primary_Action", "Timeline"]

    def unique_types(threat_list):
        types = sorted(set([x.get("type", "Unknown") for x in threat_list]))
        return ", ".join(types) if types else ""

    def avg_score(threat_list):
        scores = [int(x.get("priority_score", 0)) for x in threat_list]
        return f"{mean(scores):.2f}" if scores else "0.00"

    # Default guidance per category
    actions = {
        "Critical (12-15)": ("Immediate Response", "Within 24 hours"),
        "High (8-11)": ("Urgent Investigation", "Within 72 hours"),
        "Medium (5-7)": ("Scheduled Review", "Within 2 weeks"),
        "Low (1-4)": ("Routine Monitoring", "Ongoing"),
    }

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for cat, threat_list in categories.items():
            primary_action, timeline = actions[cat]
            writer.writerow([
                cat,
                len(threat_list),
                unique_types(threat_list),
                avg_score(threat_list),
                primary_action,
                timeline
            ])

    print(f"Risk matrix saved to: {output_file}")


if __name__ == "__main__":
    create_risk_matrix()
