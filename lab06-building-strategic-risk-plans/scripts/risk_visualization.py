#!/usr/bin/env python3
"""
Risk Management Visualization Tools
Students will complete visualization functions
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class RiskVisualization:
    def __init__(self):
        plt.style.use("default")
        sns.set_style("whitegrid")

    def create_risk_heatmap(self, alignment_df):
        """
        Create heatmap showing risk scores across conditions.

        Args:
            alignment_df: DataFrame with alignment data
        """
        # Pivot data for heatmap (risk_type vs behavior_level)
        # Use average across culture_score for a stable heatmap
        pivot_df = alignment_df.pivot_table(
            index="risk_type",
            columns="behavior_level",
            values="risk_score",
            aggfunc="mean"
        )

        plt.figure(figsize=(10, 6))

        ax = sns.heatmap(pivot_df, annot=True, fmt=".2f", linewidths=0.5)
        ax.set_title("Average Risk Score Heatmap (Risk Type vs Behavior Level)")
        ax.set_xlabel("Behavior Level")
        ax.set_ylabel("Risk Type")

        plt.tight_layout()
        plt.savefig("risk_heatmap.png")
        plt.close()

    def create_alignment_distribution(self, alignment_df):
        """Create pie chart of alignment status distribution."""
        counts = alignment_df["alignment_status"].value_counts()

        plt.figure(figsize=(7, 7))
        plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
        plt.title("Alignment Status Distribution")

        plt.tight_layout()
        plt.savefig("alignment_distribution.png")
        plt.close()

    def create_culture_impact_chart(self, alignment_df):
        """Create line chart showing culture score impact on risk."""
        grouped = alignment_df.groupby(["risk_type", "culture_score"])["risk_score"].mean().reset_index()

        plt.figure(figsize=(10, 6))
        for risk_type in grouped["risk_type"].unique():
            subset = grouped[grouped["risk_type"] == risk_type].sort_values("culture_score")
            plt.plot(subset["culture_score"], subset["risk_score"], marker="o", label=risk_type)

        plt.title("Culture Score Impact on Risk (Average Risk Score by Culture Score)")
        plt.xlabel("Culture Score")
        plt.ylabel("Average Risk Score (0-10)")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.savefig("culture_impact_chart.png")
        plt.close()


def main():
    # Load alignment data from CSV
    csv_file = "risk_alignment_matrix.csv"
    alignment_df = pd.read_csv(csv_file)

    # Initialize visualization object
    viz = RiskVisualization()

    # Create all three visualizations
    viz.create_risk_heatmap(alignment_df)
    viz.create_alignment_distribution(alignment_df)
    viz.create_culture_impact_chart(alignment_df)

    print("[INFO] Visualizations generated successfully:")
    print(" - risk_heatmap.png")
    print(" - alignment_distribution.png")
    print(" - culture_impact_chart.png")


if __name__ == "__main__":
    main()
