#!/usr/bin/env python3
"""
Security Culture Communication Plan Generator
Full Implementation
"""

import json
import os
from datetime import datetime, timedelta


class CommunicationPlan:
    def __init__(self, plan_name):
        self.plan = {
            "plan_name": plan_name,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "target_audiences": {},
            "communication_channels": [],
            "messaging_calendar": [],
            "success_metrics": []
        }

    def add_target_audience(self, name, characteristics, channels):
        self.plan["target_audiences"][name] = {
            "characteristics": characteristics,
            "preferred_channels": channels
        }

    def add_communication_channel(self, name, description, frequency):
        self.plan["communication_channels"].append({
            "name": name,
            "description": description,
            "frequency": frequency
        })

    def schedule_message(self, date, audience, channel, message_type, content):
        self.plan["messaging_calendar"].append({
            "date": date,
            "audience": audience,
            "channel": channel,
            "type": message_type,
            "content": content
        })

    def add_success_metric(self, metric_name, target, measurement):
        self.plan["success_metrics"].append({
            "metric_name": metric_name,
            "target": target,
            "measurement": measurement
        })

    def save_plan(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.plan, f, indent=4)

    def generate_summary(self):
        return {
            "audience_count": len(self.plan["target_audiences"]),
            "channel_count": len(self.plan["communication_channels"]),
            "scheduled_messages": len(self.plan["messaging_calendar"]),
            "success_metrics": len(self.plan["success_metrics"])
        }


def main():
    cp = CommunicationPlan("2026 Security Culture Communication Plan")

    # Audiences
    cp.add_target_audience(
        "Executives",
        ["Focus on ROI", "Strategic oversight", "Risk management"],
        ["Email", "Board Presentation"]
    )

    cp.add_target_audience(
        "Managers",
        ["Team leaders", "Operational focus"],
        ["Email", "Team Meetings"]
    )

    cp.add_target_audience(
        "Employees",
        ["All staff", "Operational users"],
        ["Email", "Intranet", "Training Portal"]
    )

    # Channels
    cp.add_communication_channel("Email", "Primary communication channel", "Weekly")
    cp.add_communication_channel("Intranet", "Internal announcements", "Monthly")
    cp.add_communication_channel("Town Hall", "Leadership presentations", "Quarterly")
    cp.add_communication_channel("Training Portal", "Security learning modules", "Monthly")

    # 12 months scheduling
    start = datetime.now()
    for i in range(12):
        month_date = (start + timedelta(days=30*i)).strftime("%Y-%m-%d")

        cp.schedule_message(month_date, "Executives", "Email", "Monthly Security Report",
                            "Executive security culture performance report")

        cp.schedule_message(month_date, "Managers", "Email", "Team Security Update",
                            "Manager toolkit and team metrics")

        cp.schedule_message(month_date, "Employees", "Email", "Security Awareness Tip",
                            "Monthly phishing awareness and security best practices")

    # Success metrics
    cp.add_success_metric("Email Open Rate", "75%", "Tracked via email system")
    cp.add_success_metric("Phishing Click Rate", "<5%", "Phishing simulation results")
    cp.add_success_metric("Training Completion Rate", ">90%", "LMS reporting")
    cp.add_success_metric("Incident Reporting Increase", "+20%", "SOC logs")

    cp.save_plan("data/communication_plan.json")

    summary = cp.generate_summary()
    print("\nCommunication Plan Summary:")
    for k, v in summary.items():
        print(f"{k}: {v}")

    print("\nPlan saved to data/communication_plan.json")


if __name__ == "__main__":
    main()
