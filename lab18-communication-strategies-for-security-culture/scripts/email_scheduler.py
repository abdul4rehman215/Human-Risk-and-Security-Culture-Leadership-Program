#!/usr/bin/env python3
"""
Automated Email Scheduler for Security Communications
Full Implementation
"""

import json
import os
from datetime import datetime, timedelta

from email_config import SecurityEmailSender, EmailConfig
from email_templates import SecurityEmailTemplates


class EmailScheduler:
    def __init__(self):
        self.schedule = []
        self.email_sender = None
        self.templates = None

    def initialize(self):
        """Initialize email sender and templates"""
        cfg = EmailConfig()
        self.email_sender = SecurityEmailSender(cfg.config)
        self.templates = SecurityEmailTemplates()

    def add_scheduled_email(self, send_date, audience, recipients, template_data):
        entry = {
            "send_date": send_date.strftime("%Y-%m-%d"),
            "audience": audience,
            "recipients": recipients,
            "template_data": template_data,
            "status": "pending",
            "sent_timestamp": None
        }
        self.schedule.append(entry)

    def create_monthly_schedule(self, start_date, months=12):
        """
        Create schedule:
        - Executives: Monthly
        - Managers: Bi-weekly
        - Employees: Weekly
        """
        for m in range(months):
            base = start_date + timedelta(days=30 * m)
            month_label = base.strftime("%B %Y")

            # Executives (1 per month)
            self.add_scheduled_email(
                base,
                "executive",
                ["ceo@company.local", "cfo@company.local"],
                {
                    "month": month_label,
                    "risk_reduction": 30 + (m % 10),
                    "cost_savings": str(100000 + (m * 5000)),
                    "compliance_score": 85 + (m % 10),
                    "phishing_click_rate": round(10 - (m * 0.3), 2) if (10 - (m * 0.3)) > 3 else 3,
                    "incident_reduction": 20 + (m % 5),
                    "training_completion": 90 + (m % 7),
                    "generated_date": datetime.now().strftime("%Y-%m-%d")
                }
            )

            # Managers (2 per month)
            for k in range(2):
                send_date = base + timedelta(days=15 * k)
                self.add_scheduled_email(
                    send_date,
                    "manager",
                    ["manager1@company.local", "manager2@company.local"],
                    {
                        "month": month_label,
                        "team_training_target": 95,
                        "training_completion": 88 + (m % 10),
                        "reports_count": 10 + (m % 12),
                        "phishing_click_rate": round(9 - (m * 0.25), 2) if (9 - (m * 0.25)) > 3 else 3,
                        "generated_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )

            # Employees (4 per month approx weekly)
            for w in range(4):
                send_date = base + timedelta(days=7 * w)
                self.add_scheduled_email(
                    send_date,
                    "employee",
                    ["employee1@company.local", "employee2@company.local", "employee3@company.local"],
                    {
                        "month": month_label,
                        "training_module": "Phishing Awareness Basics",
                        "checklist_link": "intranet.company.local/security-checklist",
                        "generated_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )

    def process_due_emails(self, current_date):
        sent_records = []
        for entry in self.schedule:
            if entry["status"] != "pending":
                continue

            send_date = datetime.strptime(entry["send_date"], "%Y-%m-%d")
            if send_date <= current_date:
                audience = entry["audience"]

                for recipient in entry["recipients"]:
                    subject, body = self.templates.generate_email(
                        audience, **entry["template_data"]
                    )
                    self.email_sender.send_email(recipient, subject, body)

                entry["status"] = "sent"
                entry["sent_timestamp"] = datetime.now().isoformat(timespec="seconds")
                sent_records.append(entry)

        self.email_sender.save_log("logs/email_log.json")
        return sent_records

    def save_schedule(self, filename="data/email_schedule.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.schedule, f, indent=2)

    def load_schedule(self, filename="data/email_schedule.json"):
        if not os.path.exists(filename):
            self.schedule = []
            return
        with open(filename, "r") as f:
            self.schedule = json.load(f)

    def get_schedule_summary(self):
        total = len(self.schedule)
        by_audience = {"executive": 0, "manager": 0, "employee": 0}
        sent = 0
        pending = 0

        for e in self.schedule:
            aud = e.get("audience")
            if aud in by_audience:
                by_audience[aud] += 1

            if e.get("status") == "sent":
                sent += 1
            else:
                pending += 1

        return {
            "total_scheduled": total,
            "by_audience": by_audience,
            "sent": sent,
            "pending": pending
        }


def main():
    scheduler = EmailScheduler()
    scheduler.initialize()

    start_date = datetime.now()
    scheduler.create_monthly_schedule(start_date, months=12)

    scheduler.save_schedule("data/email_schedule.json")
    print("\nSaved schedule to data/email_schedule.json")

    sent = scheduler.process_due_emails(datetime.now())
    print(f"\nProcessed due emails. Sent batches: {len(sent)}")

    summary = scheduler.get_schedule_summary()
    print("\nSchedule Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
