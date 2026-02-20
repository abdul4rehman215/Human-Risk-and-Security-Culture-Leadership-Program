#!/usr/bin/env python3
"""
Compliance Metrics Visualizer
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ComplianceVisualizer:
    def __init__(self, data_file="compliance_metrics.csv"):
        self.df = pd.read_csv(data_file)
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m", errors="coerce")
        sns.set_theme(style="whitegrid")

    def plot_department_comparison(self):
        dept = (
            self.df.groupby("department", as_index=False)["compliance_score"]
            .mean()
            .sort_values("compliance_score", ascending=False)
        )

        plt.figure(figsize=(10, 5))
        plt.bar(dept["department"], dept["compliance_score"])
        plt.axhline(80, linestyle="--", linewidth=1)
        plt.title("Average Compliance Score by Department")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("dept_comparison.png", dpi=200)
        plt.close()
        print("Saved: dept_comparison.png")

    def plot_trends(self):
        monthly = self.df.groupby("date", as_index=False).mean(numeric_only=True)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        axes[0, 0].plot(monthly["date"], monthly["training_completion_rate"], marker="o")
        axes[0, 1].plot(monthly["date"], monthly["phishing_click_rate"], marker="o")
        axes[1, 0].plot(monthly["date"], monthly["compliance_score"], marker="o")

        for ax in axes.flatten():
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True)

        axes[1, 1].axis("off")

        plt.tight_layout()
        plt.savefig("compliance_trends.png", dpi=200)
        plt.close()
        print("Saved: compliance_trends.png")

    def plot_correlation_heatmap(self):
        cols = [
            "training_completion_rate",
            "policy_acknowledgment_rate",
            "phishing_click_rate",
            "assessment_pass_rate",
            "compliance_score",
        ]
        corr = self.df[cols].corr(numeric_only=True)

        plt.figure(figsize=(9, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
        plt.tight_layout()
        plt.savefig("correlation_heatmap.png", dpi=200)
        plt.close()
        print("Saved: correlation_heatmap.png")


if __name__ == "__main__":
    visualizer = ComplianceVisualizer()
    visualizer.plot_department_comparison()
    visualizer.plot_trends()
    visualizer.plot_correlation_heatmap()
