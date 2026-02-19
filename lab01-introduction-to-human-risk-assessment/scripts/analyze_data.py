#!/usr/bin/env python3
"""
Data Analysis Script

- Calculates risk scores for all participants (using RiskScorer)
- Stores per-category and overall scores in database
- Generates charts and summary report (using RiskDashboard)
"""

import os
import sqlite3
from risk_scoring import RiskScorer
from risk_dashboard import RiskDashboard


def connect_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def analyze_all_participants(db_path: str) -> None:
    conn = connect_db(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM participants")
        participant_ids = [row[0] for row in cur.fetchall()]
    finally:
        conn.close()

    if not participant_ids:
        print("No participants found. Generate sample data or submit survey responses first.")
        return

    scorer = RiskScorer(db_path)

    for pid in participant_ids:
        category_scores, overall_score = scorer.process_participant_scores(pid)
        print(f"Participant {pid}: overall_score={overall_score} category_scores={category_scores}")

    print(f"Processed scores for {len(participant_ids)} participants")


def generate_reports(db_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    dashboard = RiskDashboard(db_path, output_dir)
    dist_path = dashboard.generate_risk_distribution_chart()
    cat_path = dashboard.generate_category_scores_chart()
    report_path = dashboard.generate_summary_report()

    print(f"Saved risk distribution chart: {dist_path}")
    print(f"Saved category scores chart: {cat_path}")
    print(f"Saved summary report: {report_path}")


if __name__ == "__main__":
    db_path = "../data/assessment.db"
    output_dir = "../reports"

    print("Analyzing participant data...")
    analyze_all_participants(db_path)

    print("Generating reports...")
    generate_reports(db_path, output_dir)

    print("Analysis complete. Check reports directory for results.")
