import pandas as pd
from datetime import datetime
import json
from data_collector import SecurityCultureDataCollector


class SecurityCultureTrendAnalyzer:
    """Analyze trends in security culture metrics over time."""

    def __init__(self, db_path='data/security_culture.db'):
        self.collector = SecurityCultureDataCollector(db_path)

    def analyze_training_trends(self, months_back=6):
        """
        Analyze training trends over time.

        Returns:
        - monthly_avg_score
        - monthly_completion_count
        - direction
        """
        days_back = int(months_back * 30)
        df = self.collector.collect_training_metrics(days_back=days_back)

        if df.empty:
            return {"monthly": [], "direction": "no_data"}

        df["month"] = df["completion_date"].dt.to_period("M").astype(str)
        monthly = df.groupby("month").agg(
            avg_score=("score", "mean"),
            completions=("score", "count")
        ).reset_index()

        monthly["avg_score"] = monthly["avg_score"].round(2)
        monthly_list = monthly.to_dict(orient="records")

        direction = "stable"
        if len(monthly) >= 2:
            if monthly["avg_score"].iloc[-1] > monthly["avg_score"].iloc[0]:
                direction = "improving"
            elif monthly["avg_score"].iloc[-1] < monthly["avg_score"].iloc[0]:
                direction = "declining"

        return {"monthly": monthly_list, "direction": direction}

    def analyze_phishing_trends(self, months_back=6):
        """
        Analyze phishing simulation trends.

        Returns:
        - monthly_click_rate
        - monthly_report_rate
        - direction_click (improving means click rate decreasing)
        - direction_report (improving means report rate increasing)
        """
        days_back = int(months_back * 30)
        df = self.collector.collect_phishing_metrics(days_back=days_back)

        if df.empty:
            return {"monthly": [], "direction_click": "no_data", "direction_report": "no_data"}

        df["month"] = df["simulation_date"].dt.to_period("M").astype(str)
        monthly = df.groupby("month").agg(
            click_rate=("clicked_link", "mean"),
            report_rate=("reported_email", "mean")
        ).reset_index()

        monthly["click_rate"] = (monthly["click_rate"] * 100).round(2)
        monthly["report_rate"] = (monthly["report_rate"] * 100).round(2)

        monthly_list = monthly.to_dict(orient="records")

        direction_click = "stable"
        direction_report = "stable"

        if len(monthly) >= 2:
            # click improving if last < first
            if monthly["click_rate"].iloc[-1] < monthly["click_rate"].iloc[0]:
                direction_click = "improving"
            elif monthly["click_rate"].iloc[-1] > monthly["click_rate"].iloc[0]:
                direction_click = "declining"

            # report improving if last > first
            if monthly["report_rate"].iloc[-1] > monthly["report_rate"].iloc[0]:
                direction_report = "improving"
            elif monthly["report_rate"].iloc[-1] < monthly["report_rate"].iloc[0]:
                direction_report = "declining"

        return {
            "monthly": monthly_list,
            "direction_click": direction_click,
            "direction_report": direction_report
        }

    def analyze_culture_score_trends(self, months_back=6):
        """
        Analyze culture score trends over time.

        Returns:
        - monthly_culture_score
        - direction
        """
        days_back = int(months_back * 30)
        df = self.collector.collect_survey_metrics(days_back=days_back)

        if df.empty:
            return {"monthly": [], "direction": "no_data"}

        df["month"] = df["survey_date"].dt.to_period("M").astype(str)
        monthly = df.groupby("month").agg(
            awareness=("awareness_score", "mean"),
            behavior=("behavior_score", "mean")
        ).reset_index()

        monthly["culture_score"] = (
            (monthly["awareness"] + monthly["behavior"]) / 2.0
        ).round(2)

        monthly_list = monthly[["month", "culture_score"]].to_dict(orient="records")

        direction = "stable"
        if len(monthly) >= 2:
            if monthly["culture_score"].iloc[-1] > monthly["culture_score"].iloc[0]:
                direction = "improving"
            elif monthly["culture_score"].iloc[-1] < monthly["culture_score"].iloc[0]:
                direction = "declining"

        return {"monthly": monthly_list, "direction": direction}

    def generate_trend_report(self, months_back=6):
        """
        Generate comprehensive trend report.
        """
        report = {
            "metadata": {
                "generated_at_utc": datetime.utcnow().isoformat() + "Z",
                "months_back": months_back
            },
            "training_trends": self.analyze_training_trends(months_back=months_back),
            "phishing_trends": self.analyze_phishing_trends(months_back=months_back),
            "culture_trends": self.analyze_culture_score_trends(months_back=months_back)
        }
        return report

    def save_report_to_json(self, report, filename='data/trend_report.json'):
        with open(filename, "w") as f:
            json.dump(report, f, indent=2, default=str)


def main():
    analyzer = SecurityCultureTrendAnalyzer()
    report = analyzer.generate_trend_report(months_back=6)
    analyzer.save_report_to_json(report, filename="data/trend_report.json")
    print("Saved trend report to data/trend_report.json")


if __name__ == "__main__":
    main()
