#!/usr/bin/env python3
"""
Communication Dashboard for Security Culture Program
Full Implementation (Text-based dashboard)
"""

import json
import os
from datetime import datetime

from communication_metrics import CommunicationMetrics
from email_scheduler import EmailScheduler


class CommunicationDashboard:
    def __init__(self):
        self.metrics = CommunicationMetrics()
        self.scheduler = EmailScheduler()

    def load_data(self):
        """
        Load metrics and schedule data
        """
        metrics_loaded = self.metrics.load_metrics("data/communication_metrics.json")

        # Load schedule file manually
        self.scheduler.schedule = []
        schedule_file = "data/email_schedule.json"

        if os.path.exists(schedule_file):
            with open(schedule_file, "r") as f:
                self.scheduler.schedule = json.load(f)

        return metrics_loaded

    def display_overview(self):
        """
        Overview dashboard:
        total emails, engagement rates, upcoming schedule
        """
        report = self.metrics.generate_report()
        totals = report["totals"]

        print("\n" + "=" * 70)
        print("SECURITY COMMUNICATION DASHBOARD")
        print("=" * 70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        print(f"Total Emails Sent   : {totals['emails_sent']}")
        print(f"Total Emails Opened : {totals['emails_opened']}")
        print(f"Total Links Clicked : {totals['links_clicked']}")
        print(f"Overall Engagement  : {totals['overall_engagement_rate_percent']}%")
        print("-" * 70)

        # Upcoming pending emails
        pending = [e for e in self.scheduler.schedule if e.get("status") == "pending"]
        pending_sorted = sorted(pending, key=lambda x: x.get("send_date", "9999-99-99"))

        print("Upcoming Scheduled Emails (Next 5):")

        if not pending_sorted:
            print("  None pending (schedule may not be created yet).")
        else:
            for e in pending_sorted[:5]:
                print(f"  - {e['send_date']} | {e['audience']} | recipients={len(e['recipients'])}")

    def display_audience_breakdown(self):
        """
        Show sent/open/click + engagement by audience
        """
        report = self.metrics.generate_report()
        aud = report["audience_breakdown"]

        print("\n" + "=" * 70)
        print("AUDIENCE BREAKDOWN")
        print("=" * 70)

        for audience, values in aud.items():
            print(f"\nAudience: {audience.upper()}")
            print("-" * 40)
            print(f"Sent      : {values['sent']}")
            print(f"Opened    : {values['opened']}")
            print(f"Clicked   : {values['clicked']}")
            print(f"Engagement: {values['engagement_rate_percent']}%")

            link_types = values.get("link_types", {})
            if link_types:
                print("Click Types:")
                for lt, count in link_types.items():
                    print(f"  - {lt}: {count}")

    def display_monthly_trends(self):
        """
        Show monthly trend data
        """
        report = self.metrics.generate_report()
        monthly = report["monthly_breakdown"]

        print("\n" + "=" * 70)
        print("MONTHLY TRENDS")
        print("=" * 70)

        if not monthly:
            print("No monthly data available yet.")
            return

        for month in sorted(monthly.keys()):
            m = monthly[month]
            sent = m.get("sent", 0)
            opened = m.get("opened", 0)
            clicked = m.get("clicked", 0)

            engagement = 0.0
            if sent > 0:
                engagement = round(((opened + clicked) / sent) * 100, 2)

            print(f"{month}: sent={sent}, opened={opened}, clicked={clicked}, engagement={engagement}%")

    def display_recommendations(self):
        """
        Generate recommendations based on engagement
        """
        overall = self.metrics.calculate_engagement_rate()
        exec_eng = self.metrics.calculate_engagement_rate("executive")
        mgr_eng = self.metrics.calculate_engagement_rate("manager")
        emp_eng = self.metrics.calculate_engagement_rate("employee")

        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)

        # Overall
        if overall < 40:
            print("• Overall engagement is LOW. Improve subject lines and clarity.")
        elif overall < 70:
            print("• Overall engagement is MODERATE. Add actionable content and clarity.")
        else:
            print("• Overall engagement is HIGH. Continue refining targeted improvements.")

        # Executive
        if exec_eng < 50:
            print("• Executives: Shorten summaries and focus on ROI + top risk metrics.")
        else:
            print("• Executives: Engagement healthy. Add quarterly strategic insights.")

        # Managers
        if mgr_eng < 50:
            print("• Managers: Provide quick toolkits and meeting-ready scripts.")
        else:
            print("• Managers: Engagement strong. Add team challenges and recognition.")

        # Employees
        if emp_eng < 50:
            print("• Employees: Add interactive tips and simple reporting guidance.")
        else:
            print("• Employees: Maintain weekly tips and add micro-quizzes.")

        print("\nSuggested next steps:")
        print("1) Review subject lines for clarity.")
        print("2) Test shorter vs longer message versions.")
        print("3) Align messages with active risk themes (phishing, MFA, passwords).")

    def generate_full_dashboard(self):
        self.display_overview()
        self.display_audience_breakdown()
        self.display_monthly_trends()
        self.display_recommendations()


def main():
    dashboard = CommunicationDashboard()
    loaded = dashboard.load_data()

    if not loaded:
        print("Metrics file not found. Run metrics script first.\n")

    dashboard.generate_full_dashboard()


if __name__ == "__main__":
    main()
