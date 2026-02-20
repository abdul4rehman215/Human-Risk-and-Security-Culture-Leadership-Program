#!/usr/bin/env python3
"""
Continuous Monitoring System
Full Implementation
Monitoring and alerting for long-term security programs
"""

import json
import datetime
import pandas as pd
import random
import os


class ProgramMonitor:
    def __init__(self, plan_path):
        self.plan = self.load_plan(plan_path)

    def load_plan(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Project plan not found. Run project_planner.py first.")
            exit(1)
        except json.JSONDecodeError:
            print("Project plan JSON invalid.")
            exit(1)

    def collect_metrics(self):
        """
        Simulated metric collection for lab purposes.
        """

        awareness_score = random.randint(40, 90)
        training_completion = random.randint(45, 95)
        incident_count = random.randint(30, 110)
        compliance_score = random.randint(60, 98)

        metrics = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "awareness_score": awareness_score,
            "training_completion": training_completion,
            "incident_count": incident_count,
            "compliance_score": compliance_score
        }

        return metrics

    def _get_targets(self):
        """
        Default targets from configuration.
        """
        return {
            "awareness_score": 85,
            "training_completion": 90,
            "incident_count": 40,
            "compliance_score": 95
        }

    def analyze_progress(self, metrics):

        targets = self._get_targets()
        analysis = {
            "timestamp": metrics["timestamp"],
            "metrics": {},
            "recommendations": []
        }

        # Awareness
        awareness_target = targets["awareness_score"]
        awareness_value = metrics["awareness_score"]
        awareness_progress = min(100, round((awareness_value / awareness_target) * 100, 2))
        awareness_status = (
            "on-track" if awareness_progress >= 90
            else "at-risk" if awareness_progress >= 75
            else "behind"
        )

        # Training Completion
        training_target = targets["training_completion"]
        training_value = metrics["training_completion"]
        training_progress = min(100, round((training_value / training_target) * 100, 2))
        training_status = (
            "on-track" if training_progress >= 90
            else "at-risk" if training_progress >= 75
            else "behind"
        )

        # Incident Count (lower is better)
        incident_target = targets["incident_count"]
        incident_value = metrics["incident_count"]

        if incident_value <= incident_target:
            incident_progress = 100
        else:
            incident_progress = max(0, round((incident_target / incident_value) * 100, 2))

        incident_status = (
            "on-track" if incident_value <= incident_target
            else "at-risk" if incident_value <= (incident_target * 1.25)
            else "behind"
        )

        # Compliance
        compliance_target = targets["compliance_score"]
        compliance_value = metrics["compliance_score"]
        compliance_progress = min(100, round((compliance_value / compliance_target) * 100, 2))
        compliance_status = (
            "on-track" if compliance_progress >= 90
            else "at-risk" if compliance_progress >= 75
            else "behind"
        )

        analysis["metrics"]["awareness_score"] = {
            "current": awareness_value,
            "target": awareness_target,
            "progress_percent": awareness_progress,
            "status": awareness_status
        }

        analysis["metrics"]["training_completion"] = {
            "current": training_value,
            "target": training_target,
            "progress_percent": training_progress,
            "status": training_status
        }

        analysis["metrics"]["incident_count"] = {
            "current": incident_value,
            "target": incident_target,
            "progress_percent": incident_progress,
            "status": incident_status
        }

        analysis["metrics"]["compliance_score"] = {
            "current": compliance_value,
            "target": compliance_target,
            "progress_percent": compliance_progress,
            "status": compliance_status
        }

        # Recommendations
        if awareness_status != "on-track":
            analysis["recommendations"].append(
                "Increase awareness campaigns and micro-learning."
            )

        if training_status != "on-track":
            analysis["recommendations"].append(
                "Follow up with managers to improve training completion."
            )

        if incident_status != "on-track":
            analysis["recommendations"].append(
                "Run targeted phishing simulations and reinforce reporting."
            )

        if compliance_status != "on-track":
            analysis["recommendations"].append(
                "Review compliance gaps and refresh policy acknowledgments."
            )

        if not analysis["recommendations"]:
            analysis["recommendations"].append(
                "Program is healthy. Continue monitoring cadence."
            )

        return analysis

    def generate_alerts(self, analysis):

        alerts = []

        priority_map = {
            "behind": "HIGH",
            "at-risk": "MEDIUM",
            "on-track": "LOW"
        }

        for metric_name, metric_data in analysis["metrics"].items():
            status = metric_data["status"]
            if status in ["behind", "at-risk"]:
                alerts.append(
                    f"[{priority_map[status]}] {metric_name} is {status}: "
                    f"current={metric_data['current']} "
                    f"target={metric_data['target']}"
                )

        if not alerts:
            alerts.append("[LOW] All metrics on-track.")

        return alerts

    def save_metrics(self, metrics, filename):

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        df_new = pd.DataFrame([metrics])

        if os.path.exists(filename):
            df_old = pd.read_csv(filename)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(filename, index=False)
        print(f"Metrics appended to {filename}")

    def generate_status_report(self):

        metrics = self.collect_metrics()
        analysis = self.analyze_progress(metrics)
        alerts = self.generate_alerts(analysis)

        report = {
            "metadata": {
                "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "report_type": "status_report"
            },
            "current_metrics": metrics,
            "analysis": analysis,
            "alerts": alerts
        }

        return report, metrics


def main():
    print("=== Program Monitoring System ===")

    monitor = ProgramMonitor("reports/project_plan.json")
    report, metrics = monitor.generate_status_report()

    os.makedirs("reports", exist_ok=True)

    with open("reports/status_report.json", "w") as f:
        json.dump(report, f, indent=4)

    monitor.save_metrics(metrics, "data/metrics_history.csv")

    print("\n--- Current Metrics ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\n--- Alerts ---")
    for a in report["alerts"]:
        print(a)

    print("\nStatus report saved to reports/status_report.json")


if __name__ == "__main__":
    main()
