#!/usr/bin/env python3
"""
ADDIE Model Training Development Framework
Complete implementation version
"""

import json
import os
import datetime
from typing import Dict


class ADDIEFramework:
    def __init__(self, project_name: str):
        """
        Initialize ADDIE project framework
        """
        self.project_name = project_name
        self.project_data = {
            "project_name": project_name,
            "created_date": datetime.datetime.now().isoformat(),
            "last_updated": None,
            "phases": {
                "analyze": {"status": "pending", "data": {}},
                "design": {"status": "pending", "data": {}},
                "develop": {"status": "pending", "data": {}},
                "implement": {"status": "pending", "data": {}},
                "evaluate": {"status": "pending", "data": {}},
            },
        }

    def save_project(self, filename: str = None):
        """Save project data to JSON file"""

        try:
            os.makedirs("data", exist_ok=True)

            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data/{self.project_name}_{timestamp}.json"

            self.project_data["last_updated"] = datetime.datetime.now().isoformat()

            with open(filename, "w") as f:
                json.dump(self.project_data, f, indent=4)

            print(f"Project saved successfully to {filename}")
            return filename

        except Exception as e:
            print(f"Error saving project: {e}")

    def load_project(self, filename: str):
        """Load existing project from file"""

        try:
            with open(filename, "r") as f:
                data = json.load(f)

            if "project_name" not in data or "phases" not in data:
                raise ValueError("Invalid project file format")

            self.project_data = data
            print("Project loaded successfully.")

        except FileNotFoundError:
            print("Project file not found.")
        except Exception as e:
            print(f"Error loading project: {e}")

    def update_phase_status(self, phase: str, status: str):
        """Update phase status"""

        valid_phases = ["analyze", "design", "develop", "implement", "evaluate"]
        valid_status = ["pending", "in_progress", "complete"]

        if phase not in valid_phases:
            print("Invalid phase name.")
            return

        if status not in valid_status:
            print("Invalid status.")
            return

        self.project_data["phases"][phase]["status"] = status
        print(f"{phase.upper()} phase updated to {status}")

    def display_project_overview(self):
        """Display project overview"""

        print("\n=== ADDIE PROJECT OVERVIEW ===")
        print(f"Project Name: {self.project_name}")
        print(f"Created: {self.project_data['created_date']}\n")

        completed = 0
        total = len(self.project_data["phases"])

        for phase, details in self.project_data["phases"].items():
            print(f"{phase.capitalize():<12} : {details['status']}")
            if details["status"] == "complete":
                completed += 1

        percent = (completed / total) * 100
        print(f"\nCompletion: {percent:.0f}%\n")


if __name__ == "__main__":
    addie = ADDIEFramework("Security_Awareness_Training")
    addie.display_project_overview()
