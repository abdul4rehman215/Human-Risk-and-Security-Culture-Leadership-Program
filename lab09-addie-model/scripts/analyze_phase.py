#!/usr/bin/env python3
"""
ADDIE Analyze Phase Implementation
"""

import json
import os
from datetime import datetime
from typing import Dict


class AnalyzePhase:
    def __init__(self):
        self.analysis_data = {
            "needs_assessment": {},
            "learner_analysis": {},
            "goals": {},
            "constraints": {},
        }

    def conduct_needs_assessment(self) -> Dict:
        print("\n=== TRAINING NEEDS ASSESSMENT ===")

        performance_gaps = input("Enter performance gaps (comma separated): ").split(",")
        business_objectives = input("Enter business objectives (comma separated): ").split(",")
        priority = input("Enter training priority (Low/Medium/High): ")

        self.analysis_data["needs_assessment"] = {
            "performance_gaps": [p.strip() for p in performance_gaps],
            "business_objectives": [b.strip() for b in business_objectives],
            "priority": priority,
        }

        return self.analysis_data["needs_assessment"]

    def analyze_learners(self) -> Dict:
        print("\n=== LEARNER ANALYSIS ===")

        roles = input("Enter learner roles (comma separated): ").split(",")
        experience = input("Enter experience level: ")
        location = input("Enter training location: ")

        self.analysis_data["learner_analysis"] = {
            "roles": [r.strip() for r in roles],
            "experience": experience,
            "location": location,
        }

        return self.analysis_data["learner_analysis"]

    def identify_goals(self) -> Dict:
        print("\n=== GOAL IDENTIFICATION ===")

        goals = input("Enter learning goals (comma separated): ").split(",")
        metrics = input("Enter success metrics (comma separated): ").split(",")
        timeline = input("Enter timeline (weeks): ")

        self.analysis_data["goals"] = {
            "learning_goals": [g.strip() for g in goals],
            "success_metrics": [m.strip() for m in metrics],
            "timeline_weeks": timeline,
        }

        return self.analysis_data["goals"]

    def document_constraints(self) -> Dict:
        print("\n=== CONSTRAINT DOCUMENTATION ===")

        budget = input("Enter budget: ")
        resources = input("Enter available resources (comma separated): ").split(",")

        self.analysis_data["constraints"] = {
            "budget": budget,
            "resources": [r.strip() for r in resources],
        }

        return self.analysis_data["constraints"]

    def generate_analysis_report(self, output_dir: str = "analyze"):
        os.makedirs(output_dir, exist_ok=True)

        json_file = f"{output_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(json_file, "w") as f:
            json.dump(self.analysis_data, f, indent=4)

        print(f"Analysis report saved to {json_file}")
        return json_file


if __name__ == "__main__":
    analyzer = AnalyzePhase()
    analyzer.conduct_needs_assessment()
    analyzer.analyze_learners()
    analyzer.identify_goals()
    analyzer.document_constraints()
    analyzer.generate_analysis_report()
