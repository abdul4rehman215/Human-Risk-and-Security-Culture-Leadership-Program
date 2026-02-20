#!/usr/bin/env python3
"""
Communication Metrics Tracking and Reporting
Full Implementation
"""

import json
import os
from datetime import datetime


class CommunicationMetrics:
    def __init__(self):
        self.metrics = {
            "emails_sent": 0,
            "emails_opened": 0,
            "links_clicked": 0,
            "by_audience": {
                "executive": {"sent": 0, "opened": 0, "clicked": 0, "link_types": {}},
                "manager": {"sent": 0, "opened": 0, "clicked": 0, "link_types": {}},
                "employee": {"sent": 0, "opened": 0, "clicked": 0, "link_types": {}}
            },
            "by_month": {}
        }

    def _month_key(self, date):
        if isinstance(date, str):
            return date[:7]
        return date.strftime("%Y-%m")

    def record_email_sent(self, audience, date):
        month = self._month_key(date)
        self.metrics["emails_sent"] += 1
        self.metrics["by_audience"][audience]["sent"] += 1
        self.metrics.setdefault("by_month", {}).setdefault(
            month, {"sent": 0, "opened": 0, "clicked": 0}
        )
        self.metrics["by_month"][month]["sent"] += 1

    def record_email_opened(self, audience, date):
        month = self._month_key(date)
        self.metrics["emails_opened"] += 1
        self.metrics["by_audience"][audience]["opened"] += 1
        self.metrics["by_month"][month]["opened"] += 1

    def record_link_clicked(self, audience, date, link_type):
        month = self._month_key(date)
        self.metrics["links_clicked"] += 1
        self.metrics["by_audience"][audience]["clicked"] += 1

        lt = self.metrics["by_audience"][audience]["link_types"]
        lt[link_type] = lt.get(link_type, 0) + 1

        self.metrics["by_month"][month]["clicked"] += 1

    def calculate_engagement_rate(self, audience=None):
        if audience is None:
            sent = self.metrics["emails_sent"]
            opened = self.metrics["emails_opened"]
            clicked = self.metrics["links_clicked"]
        else:
            sent = self.metrics["by_audience"][audience]["sent"]
            opened = self.metrics["by_audience"][audience]["opened"]
            clicked = self.metrics["by_audience"][audience]["clicked"]

        if sent == 0:
            return 0.0
        return round(((opened + clicked) / sent) * 100, 2)

    def generate_report(self):
        report = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "totals": {
                "emails_sent": self.metrics["emails_sent"],
                "emails_opened": self.metrics["emails_opened"],
                "links_clicked": self.metrics["links_clicked"],
                "overall_engagement_rate_percent": self.calculate_engagement_rate()
            },
            "audience_breakdown": {},
            "monthly_breakdown": self.metrics["by_month"]
        }

        for audience in self.metrics["by_audience"]:
            report["audience_breakdown"][audience] = {
                "sent": self.metrics["by_audience"][audience]["sent"],
                "opened": self.metrics["by_audience"][audience]["opened"],
                "clicked": self.metrics["by_audience"][audience]["clicked"],
                "engagement_rate_percent": self.calculate_engagement_rate(audience),
                "link_types": self.metrics["by_audience"][audience]["link_types"]
            }

        return report

    def save_metrics(self, filename="data/communication_metrics.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.metrics, f, indent=2)

    def load_metrics(self, filename="data/communication_metrics.json"):
        if not os.path.exists(filename):
            return False
        with open(filename, "r") as f:
            self.metrics = json.load(f)
        return True


def main():
    metrics = CommunicationMetrics()
    today = datetime.now().strftime("%Y-%m-%d")

    for _ in range(5):
        metrics.record_email_sent("executive", today)
    for _ in range(15):
        metrics.record_email_sent("manager", today)
    for _ in range(60):
        metrics.record_email_sent("employee", today)

    for _ in range(4):
        metrics.record_email_opened("executive", today)
    for _ in range(10):
        metrics.record_email_opened("manager", today)
    for _ in range(30):
        metrics.record_email_opened("employee", today)

    for _ in range(2):
        metrics.record_link_clicked("executive", today, "roi_report")
    for _ in range(5):
        metrics.record_link_clicked("manager", today, "toolkit")
    for _ in range(20):
        metrics.record_link_clicked("employee", today, "training_module")

    report = metrics.generate_report()

    print("\nCOMMUNICATION METRICS REPORT")
    print("=" * 60)
    print(json.dumps(report["totals"], indent=2))

    print("\nAudience Breakdown:")
    print(json.dumps(report["audience_breakdown"], indent=2))

    metrics.save_metrics("data/communication_metrics.json")
    print("\nSaved metrics to data/communication_metrics.json")


if __name__ == "__main__":
    main()
