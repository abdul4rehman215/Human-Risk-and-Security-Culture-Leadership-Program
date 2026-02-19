#!/usr/bin/env python3
"""
Role-Based Risk Visualization
I will create specialized role-risk charts
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


class RoleRiskVisualization:
    def __init__(self):
        plt.style.use("default")
        sns.set_style("whitegrid")

    def create_role_risk_heatmap(self, assessment_df):
        """Create heatmap of risk scores by role and risk type."""
        pivot_df = assessment_df.pivot_table(
            index="role",
            columns="risk_type",
            values="risk_score",
            aggfunc="mean"
        )

        plt.figure(figsize=(11, 6))
        ax = sns.heatmap(pivot_df, annot=True, fmt=".2f", linewidths=0.5)
        ax.set_title("Role vs Risk Type Heatmap (Risk Scores)")
        ax.set_xlabel("Risk Type")
        ax.set_ylabel("Role")

        plt.tight_layout()
        plt.savefig("role_risk_heatmap.png")
        plt.close()

    def create_priority_distribution(self, assessment_df):
        """Create stacked bar chart of priority distribution by role."""
        counts = assessment_df.groupby(["role", "priority_level"]).size().unstack(fill_value=0)

        # Ensure consistent priority order
        for col in ["critical", "high", "medium", "low"]:
            if col not in counts.columns:
                counts[col] = 0
        counts = counts[["critical", "high", "medium", "low"]]

        counts.plot(kind="bar", stacked=True, figsize=(10, 6))
        plt.title("Priority Distribution by Role")
        plt.xlabel("Role")
        plt.ylabel("Count")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig("priority_distribution.png")
        plt.close()

    def create_action_timeline(self, action_plan_file):
        """Create timeline visualization for action plan."""
        with open(action_plan_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        plan = data.get("action_plan", [])

        # Map timeline strings to numeric weeks
        timeline_map = {
            "immediate (1-2 weeks)": 2,
            "urgent (1 month)": 4,
            "planned (3 months)": 12,
            "routine (6 months)": 24,
        }

        rows = []
        for item in plan:
            rows.append({
                "priority_level": item.get("priority_level"),
                "avg_score": float(item.get("average_risk_score", 0)),
                "timeline_weeks": timeline_map.get(item.get("timeline"), 12),
                "instances": int(item.get("instances", 1)),
            })

        df = pd.DataFrame(rows)
        if df.empty:
            print("[ERROR] No action plan data found for timeline plot.")
            return

        plt.figure(figsize=(9, 6))
        plt.scatter(df["timeline_weeks"], df["avg_score"], s=df["instances"] * 40)

        for _, r in df.iterrows():
            plt.text(r["timeline_weeks"], r["avg_score"], str(r["priority_level"]), fontsize=9)

        plt.title("Action Plan Timeline vs Risk Score")
        plt.xlabel("Recommended Timeline (weeks)")
        plt.ylabel("Average Risk Score")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("action_timeline.png")
        plt.close()


def main():
    # Load assessment data
    assessment_df = pd.read_csv("role_based_risk_assessment.csv")

    # Create all visualizations
    viz = RoleRiskVisualization()
    viz.create_role_risk_heatmap(assessment_df)
    viz.create_priority_distribution(assessment_df)
    viz.create_action_timeline("prioritized_action_plan.json")

    print("[INFO] Role-based visualizations generated:")
    print(" - role_risk_heatmap.png")
    print(" - priority_distribution.png")
    print(" - action_timeline.png")


if __name__ == "__main__":
    main()
