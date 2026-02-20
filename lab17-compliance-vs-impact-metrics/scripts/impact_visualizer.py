#!/usr/bin/env python3
"""
Impact Metrics Visualizer
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ImpactVisualizer:
    def __init__(self, data_file="impact_metrics.csv"):
        self.df = pd.read_csv(data_file)
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m", errors="coerce")
        sns.set_theme(style="whitegrid")

    def plot_behavioral_trends(self):
        monthly = self.df.groupby("date", as_index=False).sum(numeric_only=True)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        axes[0, 0].plot(monthly["date"], monthly["voluntary_incident_reports"], marker="o")
        axes[0, 1].plot(monthly["date"], monthly["security_discussions_initiated"], marker="o")
        axes[1, 0].plot(monthly["date"], monthly["proactive_security_behaviors"], marker="o")
        axes[1, 1].plot(monthly["date"], monthly["peer_coaching_instances"], marker="o")

        for ax in axes.flatten():
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True)

        plt.tight_layout()
        plt.savefig("behavioral_trends.png", dpi=200)
        plt.close()
        print("Saved: behavioral_trends.png")

    def plot_maturity_progression(self):
        dept_monthly = (
            self.df.groupby(["date", "department"], as_index=False)["culture_maturity_score"]
            .mean()
        )

        plt.figure(figsize=(12, 6))
        for dept in dept_monthly["department"].unique():
            sub = dept_monthly[dept_monthly["department"] == dept]
            plt.plot(sub["date"], sub["culture_maturity_score"], marker="o", label=dept)

        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig("maturity_progression.png", dpi=200)
        plt.close()
        print("Saved: maturity_progression.png")

    def plot_incident_correlation(self):
        df = self.df.copy()
        df["proactive_sum"] = (
            df["voluntary_incident_reports"]
            + df["security_discussions_initiated"]
            + df["proactive_security_behaviors"]
            + df["peer_coaching_instances"]
        )

        plt.figure(figsize=(8, 6))
        sns.regplot(data=df, x="proactive_sum", y="security_incidents")
        plt.tight_layout()
        plt.savefig("incident_correlation.png", dpi=200)
        plt.close()
        print("Saved: incident_correlation.png")


if __name__ == "__main__":
    visualizer = ImpactVisualizer()
    visualizer.plot_behavioral_trends()
    visualizer.plot_maturity_progression()
    visualizer.plot_incident_correlation()
