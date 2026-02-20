#!/usr/bin/env python3
"""
Integrated Metrics Dashboard
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class IntegratedDashboard:
    def __init__(self):
        self.compliance = pd.read_csv("compliance_metrics.csv")
        self.impact = pd.read_csv("impact_metrics.csv")

        self.compliance["date"] = pd.to_datetime(self.compliance["date"], format="%Y-%m")
        self.impact["date"] = pd.to_datetime(self.impact["date"], format="%Y-%m")

        self.merged = pd.merge(
            self.compliance,
            self.impact,
            on=["date", "department"],
            how="inner"
        )

    def correlation_analysis(self):
        df = self.merged

        corr1 = df[["compliance_score", "culture_maturity_score"]].corr().iloc[0, 1]
        corr2 = df[["training_completion_rate", "voluntary_incident_reports"]].corr().iloc[0, 1]
        corr3 = df[["phishing_click_rate", "security_incidents"]].corr().iloc[0, 1]

        print("\n" + "=" * 72)
        print("INTEGRATED: CORRELATION ANALYSIS")
        print("=" * 72)
        print(f"Compliance vs Maturity: {corr1:.3f}")
        print(f"Training vs Voluntary Reports: {corr2:.3f}")
        print(f"Phishing vs Incidents: {corr3:.3f}")

        return corr1, corr2, corr3

    def create_executive_dashboard(self):
        df = self.merged

        monthly = df.groupby("date", as_index=False).agg(
            compliance=("compliance_score", "mean"),
            maturity=("culture_maturity_score", "mean"),
            incidents=("security_incidents", "sum"),
        )

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].plot(monthly["date"], monthly["compliance"], marker="o")
        axes[0].set_title("Compliance Score")

        axes[1].plot(monthly["date"], monthly["maturity"], marker="o")
        axes[1].set_title("Culture Maturity")

        axes[2].plot(monthly["date"], monthly["incidents"], marker="o")
        axes[2].set_title("Total Incidents")

        for ax in axes:
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True)

        plt.tight_layout()
        plt.savefig("executive_dashboard.png", dpi=200)
        plt.close()
        print("Saved: executive_dashboard.png")

    def generate_recommendations(self):
        print("\n" + "=" * 72)
        print("INTEGRATED: STRATEGIC RECOMMENDATIONS")
        print("=" * 72)
        print("- Track both compliance and impact monthly.")
        print("- Focus on departments with high incidents and phishing.")
        print("- Use culture maturity as long-term success indicator.")

        with open("integrated_recommendations.txt", "w") as f:
            f.write("STRATEGIC RECOMMENDATIONS\n")
            f.write("Track both compliance and impact monthly.\n")
            f.write("Focus on high-incident departments.\n")
            f.write("Use culture maturity as long-term indicator.\n")

        print("Saved: integrated_recommendations.txt")


if __name__ == "__main__":
    dashboard = IntegratedDashboard()
    dashboard.correlation_analysis()
    dashboard.create_executive_dashboard()
    dashboard.generate_recommendations()
