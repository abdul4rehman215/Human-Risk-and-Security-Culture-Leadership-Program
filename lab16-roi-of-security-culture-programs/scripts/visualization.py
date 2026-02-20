import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path


class SecurityROIVisualizer:
    """
    Create visualizations for ROI analysis.
    """

    def __init__(self, data_file, summary_file):
        """Initialize with data and summary files"""
        self.data_file = Path(data_file)
        self.summary_file = Path(summary_file)

        if not self.data_file.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_file}")
        if not self.summary_file.exists():
            raise FileNotFoundError(f"Summary file not found: {self.summary_file}")

        self.df = pd.read_csv(self.data_file)
        self.df["month"] = pd.to_datetime(self.df["month"], errors="coerce")

        with open(self.summary_file, "r") as f:
            self.summary = json.load(f)

        sns.set_theme(style="whitegrid")

    def create_roi_trend_chart(self, save_path):
        """
        Create ROI trend visualization with two subplots.

        Args:
            save_path: Path to save the chart
        """
        out = Path(save_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        df = self.df.copy()

        if "net_benefits" not in df.columns or "monthly_roi_pct" not in df.columns:
            df["total_benefits"] = df["incident_savings"] + df["productivity_gain"] + df["compliance_savings"]
            df["net_benefits"] = df["total_benefits"] - df["program_cost"]
            df["monthly_roi_pct"] = (df["net_benefits"] / df["program_cost"]) * 100

        df["cumulative_costs"] = df["program_cost"].cumsum()
        df["cumulative_benefits"] = df["total_benefits"].cumsum()
        df["cumulative_net_benefits"] = df["net_benefits"].cumsum()
        df["cumulative_roi_pct"] = (df["cumulative_net_benefits"] / df["cumulative_costs"]) * 100

        fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        axes[0].plot(df["month"], df["monthly_roi_pct"], marker="o", linewidth=2)
        axes[0].axhline(0, linestyle="--", linewidth=1)
        axes[0].set_title("Monthly ROI Trend")
        axes[0].set_ylabel("Monthly ROI (%)")
        axes[0].grid(True)

        axes[1].plot(df["month"], df["cumulative_roi_pct"], marker="o", linewidth=2)
        axes[1].axhline(0, linestyle="--", linewidth=1)
        axes[1].set_title("Cumulative ROI Trend")
        axes[1].set_ylabel("Cumulative ROI (%)")
        axes[1].set_xlabel("Month")
        axes[1].grid(True)

        plt.tight_layout()
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"Saved ROI trend chart: {out.resolve()}")

    def create_cost_benefit_analysis(self, save_path):
        """
        Create cost vs benefit comparison charts.

        Args:
            save_path: Path to save the chart
        """
        out = Path(save_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        df = self.df.copy()
        df["total_benefits"] = df["incident_savings"] + df["productivity_gain"] + df["compliance_savings"]
        df["net_benefits"] = df["total_benefits"] - df["program_cost"]
        df["cumulative_costs"] = df["program_cost"].cumsum()
        df["cumulative_benefits"] = df["total_benefits"].cumsum()

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        axes[0, 0].bar(df["month"], df["program_cost"], label="Program Cost")
        axes[0, 0].bar(df["month"], df["total_benefits"], alpha=0.7, label="Total Benefits")
        axes[0, 0].set_title("Monthly Costs vs Benefits")
        axes[0, 0].set_ylabel("USD")
        axes[0, 0].legend()
        axes[0, 0].tick_params(axis='x', rotation=45)

        axes[0, 1].plot(df["month"], df["cumulative_costs"], marker="o", label="Cumulative Costs")
        axes[0, 1].plot(df["month"], df["cumulative_benefits"], marker="o", label="Cumulative Benefits")
        axes[0, 1].set_title("Cumulative Costs vs Benefits")
        axes[0, 1].set_ylabel("USD")
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis='x', rotation=45)

        total_incident_savings = df["incident_savings"].sum()
        total_productivity = df["productivity_gain"].sum()
        total_compliance = df["compliance_savings"].sum()

        axes[1, 0].pie(
            [total_incident_savings, total_productivity, total_compliance],
            labels=["Incident Savings", "Productivity Gain", "Compliance Savings"],
            autopct="%1.1f%%",
            startangle=90
        )
        axes[1, 0].set_title("Benefit Breakdown (2 Years)")

        colors = ["green" if x >= 0 else "red" for x in df["net_benefits"]]
        axes[1, 1].bar(df["month"], df["net_benefits"], color=colors)
        axes[1, 1].axhline(0, linestyle="--", linewidth=1)
        axes[1, 1].set_title("Net Benefits Over Time")
        axes[1, 1].set_ylabel("USD")
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"Saved cost-benefit analysis chart: {out.resolve()}")

    def create_security_metrics_dashboard(self, save_path):
        """
        Create dashboard showing security metric improvements.

        Args:
            save_path: Path to save the dashboard
        """
        out = Path(save_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        df = self.df.copy()

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        axes[0, 0].plot(df["month"], df["phishing_success_rate"] * 100, marker="o")
        axes[0, 0].set_title("Phishing Success Rate Reduction")
        axes[0, 0].set_ylabel("Phishing Success Rate (%)")
        axes[0, 0].tick_params(axis='x', rotation=45)

        axes[0, 1].plot(df["month"], df["security_incidents"], marker="o")
        axes[0, 1].set_title("Security Incidents Reduction")
        axes[0, 1].set_ylabel("Monthly Incidents")
        axes[0, 1].tick_params(axis='x', rotation=45)

        axes[1, 0].plot(df["month"], df["compliance_rate"] * 100, marker="o")
        axes[1, 0].set_title("Compliance Rate Improvement")
        axes[1, 0].set_ylabel("Compliance Rate (%)")
        axes[1, 0].tick_params(axis='x', rotation=45)

        phishing_norm = 1 - (df["phishing_success_rate"] - df["phishing_success_rate"].min()) / (
            (df["phishing_success_rate"].max() - df["phishing_success_rate"].min()) + 1e-9
        )
        incidents_norm = 1 - (df["security_incidents"] - df["security_incidents"].min()) / (
            (df["security_incidents"].max() - df["security_incidents"].min()) + 1e-9
        )
        compliance_norm = (df["compliance_rate"] - df["compliance_rate"].min()) / (
            (df["compliance_rate"].max() - df["compliance_rate"].min()) + 1e-9
        )

        composite_score = (0.4 * phishing_norm + 0.3 * incidents_norm + 0.3 * compliance_norm) * 100
        axes[1, 1].plot(df["month"], composite_score, marker="o")
        axes[1, 1].set_title("Composite Security Score (Higher is Better)")
        axes[1, 1].set_ylabel("Score (0-100)")
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"Saved security metrics dashboard: {out.resolve()}")

    def create_executive_summary_chart(self, save_path):
        """
        Create executive summary visualization.

        Args:
            save_path: Path to save the chart
        """
        out = Path(save_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        df = self.df.copy()
        df["total_benefits"] = df["incident_savings"] + df["productivity_gain"] + df["compliance_savings"]
        df["net_benefits"] = df["total_benefits"] - df["program_cost"]
        df["monthly_roi_pct"] = (df["net_benefits"] / df["program_cost"]) * 100

        final_roi = self.summary.get("final_cumulative_roi_pct", 0)
        avg_roi = self.summary.get("average_monthly_roi_pct", 0)
        best_roi = self.summary.get("best_monthly_roi_pct", 0)

        investment = self.summary.get("total_investment", 0)
        benefits = self.summary.get("total_benefits", 0)
        net = self.summary.get("total_net_benefits", 0)

        payback_months = self.summary.get("months_to_payback", None)
        payback_date = self.summary.get("payback_date", None)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        axes[0, 0].bar(["Final ROI", "Avg Monthly ROI", "Best Monthly ROI"], [final_roi, avg_roi, best_roi])
        axes[0, 0].set_title("ROI Metrics (%)")
        axes[0, 0].set_ylabel("ROI (%)")
        axes[0, 0].axhline(0, linestyle="--", linewidth=1)

        axes[0, 1].bar(["Investment", "Benefits", "Net Benefits"], [investment, benefits, net])
        axes[0, 1].set_title("Financial Summary (USD)")
        axes[0, 1].set_ylabel("USD")

        axes[1, 0].plot(df["month"], df["net_benefits"].cumsum(), marker="o")
        axes[1, 0].axhline(0, linestyle="--", linewidth=1)
        axes[1, 0].set_title("Cumulative Net Benefits (Payback when > 0)")
        axes[1, 0].set_ylabel("USD")
        axes[1, 0].tick_params(axis='x', rotation=45)
        if payback_months is not None:
            axes[1, 0].text(
                0.02, 0.95,
                f"Payback: {payback_months} months\nDate: {payback_date}",
                transform=axes[1, 0].transAxes,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
            )

        axes[1, 1].axis("off")
        summary_text = (
            "Executive Summary\n"
            "-----------------\n"
            f"Total Investment: ${investment:,.2f}\n"
            f"Total Benefits:   ${benefits:,.2f}\n"
            f"Net Benefits:     ${net:,.2f}\n"
            f"Final ROI:        {final_roi:.2f}%\n"
            f"Avg Monthly ROI:  {avg_roi:.2f}%\n"
            f"Payback Period:   {payback_months if payback_months is not None else 'N/A'} months\n"
            f"Payback Date:     {payback_date if payback_date is not None else 'N/A'}\n"
        )
        axes[1, 1].text(0.02, 0.98, summary_text, va="top", fontsize=12)

        plt.tight_layout()
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"Saved executive summary chart: {out.resolve()}")


def main():
    """Generate all visualizations"""
    visualizer = SecurityROIVisualizer(
        "../data/security_metrics.csv",
        "../reports/roi_summary.json"
    )

    visualizer.create_roi_trend_chart("../visualizations/roi_trend_chart.png")
    visualizer.create_cost_benefit_analysis("../visualizations/cost_benefit_analysis.png")
    visualizer.create_security_metrics_dashboard("../visualizations/security_metrics_dashboard.png")
    visualizer.create_executive_summary_chart("../visualizations/executive_summary.png")


if __name__ == "__main__":
    main()
