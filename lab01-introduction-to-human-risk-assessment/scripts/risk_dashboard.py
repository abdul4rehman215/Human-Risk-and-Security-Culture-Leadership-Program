#!/usr/bin/env python3
"""
Risk Assessment Dashboard
"""

import os
import sqlite3
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class RiskDashboard:
    def __init__(self, db_path: str, output_dir: str):
        self.db_path = db_path
        self.output_dir = output_dir

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def generate_risk_distribution_chart(self) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        conn = self._connect()
        try:
            df = pd.read_sql_query(
                """
                SELECT risk_level, COUNT(*) as count
                FROM risk_scores
                WHERE category = 'overall'
                GROUP BY risk_level
                """,
                conn,
            )
        finally:
            conn.close()

        out_path = os.path.join(self.output_dir, "risk_distribution.png")

        if df.empty:
            plt.figure()
            plt.title("Risk Level Distribution (No Data)")
            plt.text(0.5, 0.5, "No overall scores found", ha="center", va="center")
            plt.axis("off")
            plt.savefig(out_path, bbox_inches="tight")
            plt.close()
            return out_path

        plt.figure()
        plt.pie(df["count"], labels=df["risk_level"], autopct="%1.1f%%", startangle=90)
        plt.title("Overall Risk Level Distribution")
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        return out_path

    def generate_category_scores_chart(self) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        conn = self._connect()
        try:
            df = pd.read_sql_query(
                """
                SELECT category, AVG(score) as avg_score
                FROM risk_scores
                WHERE category != 'overall'
                GROUP BY category
                ORDER BY category
                """,
                conn,
            )
        finally:
            conn.close()

        out_path = os.path.join(self.output_dir, "category_scores.png")

        if df.empty:
            plt.figure()
            plt.title("Average Category Scores (No Data)")
            plt.text(0.5, 0.5, "No category scores found", ha="center", va="center")
            plt.axis("off")
            plt.savefig(out_path, bbox_inches="tight")
            plt.close()
            return out_path

        plt.figure(figsize=(10, 5))
        sns.barplot(data=df, x="category", y="avg_score")
        plt.xticks(rotation=30, ha="right")
        plt.ylim(0, 100)
        plt.title("Average Scores by Category (Higher = Lower Risk)")
        plt.ylabel("Average Score (0-100)")
        plt.xlabel("Category")
        plt.tight_layout()
        plt.savefig(out_path, bbox_inches="tight")
        plt.close()
        return out_path

    def generate_summary_report(self) -> str:
        os.makedirs(self.output_dir, exist_ok=True)
        out_path = os.path.join(self.output_dir, "summary_report.md")

        conn = self._connect()
        try:
            overall_df = pd.read_sql_query(
                "SELECT score, risk_level FROM risk_scores WHERE category = 'overall'",
                conn,
            )
            cat_df = pd.read_sql_query(
                "SELECT category, score FROM risk_scores WHERE category != 'overall'",
                conn,
            )
            participant_count_df = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM participants",
                conn,
            )
        finally:
            conn.close()

        participant_count = int(participant_count_df["count"].iloc[0]) if not participant_count_df.empty else 0

        lines: List[str] = []
        lines.append("# Human Risk Assessment - Summary Report")
        lines.append("")
        lines.append(f"- Total participants in database: **{participant_count}**")
        lines.append("")

        if not overall_df.empty:
            lines.append("## Overall Risk Results")
            lines.append("")
            lines.append(f"- Overall average score: **{overall_df['score'].mean():.2f}**")
            lines.append(f"- Overall min score: **{overall_df['score'].min()}**")
            lines.append(f"- Overall max score: **{overall_df['score'].max()}**")
            lines.append("")

            dist = overall_df["risk_level"].value_counts(normalize=True) * 100
            lines.append("### Risk Level Distribution")
            lines.append("")
            for level, pct in dist.items():
                lines.append(f"- {level}: **{pct:.1f}%**")
            lines.append("")

        if not cat_df.empty:
            lines.append("## Category Results")
            lines.append("")
            cat_avg = cat_df.groupby("category")["score"].mean().sort_values(ascending=False)
            for cat, avg in cat_avg.items():
                lines.append(f"- {cat}: **{avg:.2f}**")
            lines.append("")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return out_path


if __name__ == "__main__":
    dashboard = RiskDashboard("../data/assessment.db", "../reports")
    print("Dashboard system initialized")
