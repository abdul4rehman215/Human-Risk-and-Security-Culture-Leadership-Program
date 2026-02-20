#!/usr/bin/env python3
"""
ADDIE Implement Phase
Implementation tracking and deployment planning
"""

import json
import os
from datetime import datetime
from typing import Dict


class ImplementPhase:
    def __init__(self):
        self.implement_data = {
            "deployment": {},
            "participant_tracking": {},
            "support_logs": [],
            "completion_data": {},
        }

    def plan_deployment(self):
        """Plan training deployment"""
        print("\n=== IMPLEMENT: DEPLOYMENT PLANNING ===")

        start_date = input("Enter deployment start date (YYYY-MM-DD): ").strip()
        sessions = input("Enter number of sessions: ").strip()
        delivery_platform = input("Enter delivery platform (e.g., LMS): ").strip()

        self.implement_data["deployment"] = {
            "start_date": start_date,
            "sessions": sessions,
            "delivery_platform": delivery_platform,
            "systems_tested": True,
            "facilitator_briefing_complete": True,
        }

        return self.implement_data["deployment"]

    def track_participants(self):
        """Track participant enrollment and progress"""
        print("\n=== IMPLEMENT: PARTICIPANT TRACKING ===")

        participants_raw = input("Enter participant names (comma separated): ").split(",")
        participants = [p.strip() for p in participants_raw if p.strip()]

        tracking = {}
        for p in participants:
            tracking[p] = {
                "enrolled": True,
                "progress_percent": 0,
                "completed": False,
                "attendance": [],
            }

        self.implement_data["participant_tracking"] = tracking
        return tracking

    def provide_support(self):
        """Manage learner support"""
        print("\n=== IMPLEMENT: SUPPORT LOGGING ===")
        print("Enter support tickets. Type 'done' when finished.\n")

        while True:
            issue = input("Support issue (or 'done'): ").strip()
            if issue.lower() == "done":
                break

            resolution = input("Resolution: ").strip()

            self.implement_data["support_logs"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "issue": issue,
                    "resolution": resolution,
                }
            )

        return self.implement_data["support_logs"]

    def update_completion(self):
        """Update completion data (manual progress entry)"""
        print("\n=== IMPLEMENT: COMPLETION UPDATE ===")

        tracking = self.implement_data.get("participant_tracking", {})
        if not tracking:
            print("No participants found. Run track_participants() first.")
            return {}

        for name in tracking.keys():
            progress = input(f"Enter progress percent for {name} (0-100): ").strip()

            try:
                progress_val = int(progress)
            except ValueError:
                progress_val = 0

            tracking[name]["progress_percent"] = max(0, min(100, progress_val))
            tracking[name]["completed"] = tracking[name]["progress_percent"] >= 100

        completion_rate = 0
        total = len(tracking)
        completed = sum(1 for n in tracking if tracking[n]["completed"])

        if total > 0:
            completion_rate = (completed / total) * 100

        self.implement_data["completion_data"] = {
            "total_participants": total,
            "completed": completed,
            "completion_rate_percent": completion_rate,
        }

        return self.implement_data["completion_data"]

    def save_implementation_report(self, output_dir: str = "implement"):
        """Save implement phase data to JSON + text"""
        os.makedirs(output_dir, exist_ok=True)

        json_path = f"{output_dir}/implement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        txt_path = json_path.replace(".json", ".txt")

        with open(json_path, "w") as f:
            json.dump(self.implement_data, f, indent=4)

        with open(txt_path, "w") as f:
            f.write("=== ADDIE IMPLEMENTATION REPORT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(json.dumps(self.implement_data, indent=4))
            f.write("\n")

        print(f"Implementation JSON saved to {json_path}")
        print(f"Implementation text report saved to {txt_path}")

        return json_path, txt_path


if __name__ == "__main__":
    implementer = ImplementPhase()
    implementer.plan_deployment()
    implementer.track_participants()
    implementer.provide_support()
    implementer.update_completion()
    implementer.save_implementation_report()
