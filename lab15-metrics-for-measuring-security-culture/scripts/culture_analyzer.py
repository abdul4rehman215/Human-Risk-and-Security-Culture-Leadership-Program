import pandas as pd
import numpy as np
from datetime import datetime
import json
from data_collector import SecurityCultureDataCollector


class SecurityCultureAnalyzer:
    """Analyze security culture metrics and generate insights."""

    def __init__(self, db_path='data/security_culture.db'):
        self.collector = SecurityCultureDataCollector(db_path)

    def calculate_training_effectiveness(self, days_back=90):
        """
        Calculate training effectiveness metrics.

        Returns dictionary with:
        - average_score
        - completion_count
        - score_by_department
        """
        df = self.collector.collect_training_metrics(days_back=days_back)
        if df.empty:
            return {
                "average_score": 0,
                "completion_count": 0,
                "score_by_department": {}
            }

        avg_score = float(df["score"].mean())
        completion_count = int(len(df))

        by_dept = df.groupby("department")["score"].mean().round(2).to_dict()
        by_dept = {k: float(v) for k, v in by_dept.items()}

        return {
            "average_score": round(avg_score, 2),
            "completion_count": completion_count,
            "score_by_department": by_dept
        }

    def calculate_phishing_resilience(self, days_back=90):
        """
        Calculate phishing resilience metrics.

        Returns dictionary with:
        - click_rate (percentage)
        - report_rate (percentage)
        - click_rate_by_department
        - report_rate_by_department
        """
        df = self.collector.collect_phishing_metrics(days_back=days_back)
        if df.empty:
            return {
                "click_rate": 0,
                "report_rate": 0,
                "click_rate_by_department": {},
                "report_rate_by_department": {}
            }

        click_rate = float(df["clicked_link"].mean() * 100.0)
        report_rate = float(df["reported_email"].mean() * 100.0)

        click_by_dept = (df.groupby("department")["clicked_link"].mean() * 100.0).round(2).to_dict()
        report_by_dept = (df.groupby("department")["reported_email"].mean() * 100.0).round(2).to_dict()

        click_by_dept = {k: float(v) for k, v in click_by_dept.items()}
        report_by_dept = {k: float(v) for k, v in report_by_dept.items()}

        return {
            "click_rate": round(click_rate, 2),
            "report_rate": round(report_rate, 2),
            "click_rate_by_department": click_by_dept,
            "report_rate_by_department": report_by_dept
        }

    def calculate_culture_score(self, days_back=90):
        """
        Calculate overall security culture score.

        Returns dictionary with:
        - overall_culture_score (1-10)
        - awareness_score
        - behavior_score
        - culture_by_department
        """
        df = self.collector.collect_survey_metrics(days_back=days_back)
        if df.empty:
            return {
                "overall_culture_score": 0,
                "awareness_score": 0,
                "behavior_score": 0,
                "culture_by_department": {}
            }

        awareness = float(df["awareness_score"].mean())
        behavior = float(df["behavior_score"].mean())

        # Overall culture score: average of awareness and behavior (1-10)
        overall = (awareness + behavior) / 2.0

        # By department
        dept_scores = df.groupby("department").apply(
            lambda g: float(((g["awareness_score"].mean() + g["behavior_score"].mean()) / 2.0))
        ).round(2).to_dict()

        dept_scores = {k: float(v) for k, v in dept_scores.items()}

        return {
            "overall_culture_score": round(overall, 2),
            "awareness_score": round(awareness, 2),
            "behavior_score": round(behavior, 2),
            "culture_by_department": dept_scores
        }

    def calculate_incident_summary(self, days_back=90):
        """
        Additional helper: summarize incidents.

        Returns:
        - total_incidents
        - incidents_by_type
        - incidents_by_severity
        - incidents_by_department
        """
        df = self.collector.collect_incident_metrics(days_back=days_back)
        if df.empty:
            return {
                "total_incidents": 0,
                "incidents_by_type": {},
                "incidents_by_severity": {},
                "incidents_by_department": {}
            }

        total = int(len(df))
        by_type = df["incident_type"].value_counts().to_dict()
        by_sev = df["severity"].value_counts().to_dict()

        # Department may contain NaN if incident not tied to employee
        df["department"] = df["department"].fillna("Unknown")
        by_dept = df["department"].value_counts().to_dict()

        by_type = {k: int(v) for k, v in by_type.items()}
        by_sev = {k: int(v) for k, v in by_sev.items()}
        by_dept = {k: int(v) for k, v in by_dept.items()}

        return {
            "total_incidents": total,
            "incidents_by_type": by_type,
            "incidents_by_severity": by_sev,
            "incidents_by_department": by_dept
        }

    def generate_comprehensive_report(self, days_back=90):
        """
        Generate complete security culture report.

        Calls all metric calculations, includes metadata.
        """
        report = {
            "metadata": {
                "generated_at_utc": datetime.utcnow().isoformat() + "Z",
                "period_days": days_back
            },
            "training_effectiveness": self.calculate_training_effectiveness(days_back=days_back),
            "phishing_resilience": self.calculate_phishing_resilience(days_back=days_back),
            "culture_score": self.calculate_culture_score(days_back=days_back),
            "incident_summary": self.calculate_incident_summary(days_back=days_back)
        }
        return report

    def save_report_to_json(self, report, filename='data/culture_report.json'):
        """Save report to JSON file."""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)


def main():
    analyzer = SecurityCultureAnalyzer()
    report = analyzer.generate_comprehensive_report(days_back=90)
    analyzer.save_report_to_json(report, filename='data/culture_report.json')
    print("Saved report to data/culture_report.json")


if __name__ == "__main__":
    main()
