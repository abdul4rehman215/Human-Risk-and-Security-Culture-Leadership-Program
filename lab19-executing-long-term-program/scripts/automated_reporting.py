#!/usr/bin/env python3
"""
Automated Reporting System
Full Implementation
Creates automated reports for stakeholders and generates charts
"""

import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os


class AutomatedReporter:
    def __init__(self, metrics_path):
        self.metrics = self.load_metrics(metrics_path)

    def load_metrics(self, path):
        try:
            df = pd.read_csv(path)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df
        except FileNotFoundError:
            print("Metrics history not found. Run monitoring_system.py first.")
            exit(1)
        except Exception as e:
            print(f"Failed to load metrics: {e}")
            exit(1)

    def create_executive_summary(self):
        """
        High-level summary for executives.
        """
        latest = self.metrics.iloc[-1]
        avg_awareness = float(round(self.metrics["awareness_score"].mean(), 2))
        avg_training = float(round(self.metrics["training_completion"].mean(), 2))
        avg_incidents = float(round(self.metrics["incident_count"].mean(), 2))
        avg_compliance = float(round(self.metrics["compliance_score"].mean(), 2))

        # Simple health score formula (0-100)
        # higher awareness/training/compliance, lower incidents
        incident_component = max(0, 100 - (avg_incidents / 2))
        health_score = round((avg_awareness + avg_training + avg_compliance + incident_component) / 4, 2)

        summary = {
            "report_generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "program_health_score": health_score,
            "latest_snapshot": {
                "timestamp": str(latest["timestamp"]),
                "awareness_score": int(latest["awareness_score"]),
                "training_completion": int(latest["training_completion"]),
                "incident_count": int(latest["incident_count"]),
                "compliance_score": int(latest["compliance_score"])
            },
            "key_achievements": [
                "Continuous metric tracking operational",
                "Status reporting automated",
                "Trends captured for stakeholder review"
            ],
            "critical_issues": [],
            "recommendations": []
        }

        # basic issue triggers
        if latest["training_completion"] < 75:
            summary["critical_issues"].append("Training completion is below 75% - requires immediate action.")
            summary["recommendations"].append("Escalate training completion to department heads and add reminders.")

        if latest["awareness_score"] < 70:
            summary["critical_issues"].append("Awareness score below 70 - increase awareness campaigns.")
            summary["recommendations"].append("Increase targeted awareness messaging and microlearning.")

        if latest["incident_count"] > 60:
            summary["critical_issues"].append("Incident count is high - strengthen controls and phishing resistance.")
            summary["recommendations"].append("Run phishing simulations and refresh incident reporting training.")

        if latest["compliance_score"] < 80:
            summary["critical_issues"].append("Compliance score below 80 - policy reinforcement required.")
            summary["recommendations"].append("Perform policy refresh and improve acknowledgment process.")

        if not summary["critical_issues"]:
            summary["critical_issues"].append("No critical issues detected.")
            summary["recommendations"].append("Maintain current cadence and review quarterly objectives.")

        return summary

    def create_detailed_report(self):
        """
        Detailed technical report.
        """
        report = {
            "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "records_analyzed": int(len(self.metrics)),
            "metric_trends": {},
            "analysis": {}
        }

        for col in ["awareness_score", "training_completion", "incident_count", "compliance_score"]:
            report["metric_trends"][col] = {
                "min": float(self.metrics[col].min()),
                "max": float(self.metrics[col].max()),
                "avg": float(round(self.metrics[col].mean(), 2)),
                "latest": float(self.metrics.iloc[-1][col])
            }

        # trend direction: compare last 3 vs first 3
        if len(self.metrics) >= 6:
            first = self.metrics.head(3)
            last = self.metrics.tail(3)
            report["analysis"]["trend_direction"] = {
                "awareness_score": "improving" if last["awareness_score"].mean() > first["awareness_score"].mean() else "declining",
                "training_completion": "improving" if last["training_completion"].mean() > first["training_completion"].mean() else "declining",
                "incident_count": "improving" if last["incident_count"].mean() < first["incident_count"].mean() else "declining",
                "compliance_score": "improving" if last["compliance_score"].mean() > first["compliance_score"].mean() else "declining"
            }
        else:
            report["analysis"]["trend_direction"] = "Not enough data for trend direction (need >= 6 records)."

        report["analysis"]["completed_milestones"] = [
            "Strategy created",
            "Project plan created",
            "Monitoring enabled",
            "Automated reporting enabled"
        ]

        report["analysis"]["resource_utilization"] = {
            "note": "Lab environment uses simulated data; resource utilization tracking can be integrated with time tracking tools."
        }

        return report

    def generate_trend_charts(self, output_dir):
        """
        Create visualization charts for metrics.
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Awareness trend
        plt.figure()
        plt.plot(self.metrics["timestamp"], self.metrics["awareness_score"], marker="o")
        plt.title("Awareness Score Over Time")
        plt.xlabel("Date")
        plt.ylabel("Awareness Score")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "awareness_trend.png"))
        plt.close()

        # Training completion trend
        plt.figure()
        plt.bar(self.metrics["timestamp"].dt.strftime("%Y-%m-%d"), self.metrics["training_completion"])
        plt.title("Training Completion Over Time")
        plt.xlabel("Date")
        plt.ylabel("Completion %")
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "training_completion_trend.png"))
        plt.close()

        # Incident reduction trend
        plt.figure()
        plt.plot(self.metrics["timestamp"], self.metrics["incident_count"], marker="o")
        plt.title("Incident Count Over Time")
        plt.xlabel("Date")
        plt.ylabel("Incident Count")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "incident_trend.png"))
        plt.close()

        # Compliance trend
        plt.figure()
        plt.plot(self.metrics["timestamp"], self.metrics["compliance_score"], marker="o")
        plt.title("Compliance Score Over Time")
        plt.xlabel("Date")
        plt.ylabel("Compliance Score")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "compliance_trend.png"))
        plt.close()

        print(f"Charts saved to {output_dir}")

    def create_stakeholder_report(self, stakeholder_type):
        """
        Customized report for stakeholder: executive, technical, hr
        """
        stakeholder_type = stakeholder_type.lower()
        base = self.create_detailed_report()

        if stakeholder_type == "executive":
            return {"stakeholder": "executive", "summary": self.create_executive_summary()}

        if stakeholder_type == "hr":
            hr_focus = {
                "stakeholder": "hr",
                "focus_metrics": {
                    "training_completion_avg": float(round(self.metrics["training_completion"].mean(), 2)),
                    "awareness_score_avg": float(round(self.metrics["awareness_score"].mean(), 2))
                },
                "recommendations": [
                    "Coordinate reminders for incomplete training",
                    "Support communication campaigns for behavior change",
                    "Work with managers for department accountability"
                ]
            }
            return hr_focus

        # default technical
        tech_focus = {
            "stakeholder": "technical",
            "details": base,
            "recommendations": [
                "Integrate metrics with SIEM/ticketing systems",
                "Automate incident feed into dashboard",
                "Enhance detection and reporting workflows"
            ]
        }
        return tech_focus

    def export_reports(self, output_dir):
        """
        Export executive + detailed + stakeholder reports and charts.
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        executive = self.create_executive_summary()
        detailed = self.create_detailed_report()
        stakeholder_exec = self.create_stakeholder_report("executive")
        stakeholder_hr = self.create_stakeholder_report("hr")
        stakeholder_tech = self.create_stakeholder_report("technical")

        with open(os.path.join(output_dir, "executive_summary.json"), "w") as f:
            json.dump(executive, f, indent=4, default=str)

        with open(os.path.join(output_dir, "detailed_report.json"), "w") as f:
            json.dump(detailed, f, indent=4, default=str)

        with open(os.path.join(output_dir, "stakeholder_executive.json"), "w") as f:
            json.dump(stakeholder_exec, f, indent=4, default=str)

        with open(os.path.join(output_dir, "stakeholder_hr.json"), "w") as f:
            json.dump(stakeholder_hr, f, indent=4, default=str)

        with open(os.path.join(output_dir, "stakeholder_technical.json"), "w") as f:
            json.dump(stakeholder_tech, f, indent=4, default=str)

        self.generate_trend_charts(os.path.join(output_dir, "charts"))

        print(f"Reports exported to {output_dir}")


def main():
    print("=== Automated Reporting System ===")

    reporter = AutomatedReporter("data/metrics_history.csv")
    reporter.export_reports("reports/automated_reports")

    exec_summary = reporter.create_executive_summary()
    print("\n--- Executive Summary Preview ---")
    print("Program Health Score:", exec_summary["program_health_score"])
    print("Critical Issues:", exec_summary["critical_issues"])


if __name__ == "__main__":
    main()
