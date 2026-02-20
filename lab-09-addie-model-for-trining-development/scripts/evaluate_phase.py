#!/usr/bin/env python3
"""
ADDIE Evaluate Phase
Evaluation methods using Kirkpatrick levels
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class EvaluatePhase:
    def __init__(self):
        self.evaluation_data = {
            "kirkpatrick_level1": {},  # Reaction
            "kirkpatrick_level2": {},  # Learning
            "kirkpatrick_level3": {},  # Behavior
            "kirkpatrick_level4": {},  # Results
            "recommendations": [],
        }

    def evaluate_reaction(self):
        """Level 1: Evaluate learner reactions"""
        print("\n=== EVALUATE: LEVEL 1 (REACTION) ===")

        avg_rating = input("Enter average satisfaction rating (1-5): ").strip()
        top_feedback = input("Enter top feedback themes (comma separated): ").split(",")

        try:
            avg_rating_val = float(avg_rating)
        except ValueError:
            avg_rating_val = 0.0

        self.evaluation_data["kirkpatrick_level1"] = {
            "avg_satisfaction_rating": avg_rating_val,
            "feedback_themes": [t.strip() for t in top_feedback if t.strip()],
            "improvement_areas": [],
        }

        if avg_rating_val < 4.0:
            self.evaluation_data["kirkpatrick_level1"]["improvement_areas"].append(
                "Improve engagement and clarity based on participant feedback."
            )

        return self.evaluation_data["kirkpatrick_level1"]

    def evaluate_learning(self):
        """Level 2: Measure learning outcomes"""
        print("\n=== EVALUATE: LEVEL 2 (LEARNING) ===")

        pre_avg = input("Enter average pre-test score percent: ").strip()
        post_avg = input("Enter average post-test score percent: ").strip()

        try:
            pre_val = float(pre_avg)
        except ValueError:
            pre_val = 0.0

        try:
            post_val = float(post_avg)
        except ValueError:
            post_val = 0.0

        improvement = post_val - pre_val

        self.evaluation_data["kirkpatrick_level2"] = {
            "pre_test_avg_percent": pre_val,
            "post_test_avg_percent": post_val,
            "improvement_percent_points": improvement,
            "achievement_rate": "Calculated via LMS if available",
            "knowledge_gaps": [],
        }

        if post_val < 80:
            self.evaluation_data["kirkpatrick_level2"]["knowledge_gaps"].append(
                "Post-test average below target; reinforce weak areas with additional practice."
            )

        return self.evaluation_data["kirkpatrick_level2"]

    def evaluate_behavior(self):
        """Level 3: Assess behavior change"""
        print("\n=== EVALUATE: LEVEL 3 (BEHAVIOR) ===")

        observation_window = input("Enter behavior observation window (e.g., 30 days): ").strip()
        supervisor_feedback = input("Enter supervisor feedback summary: ").strip()

        self.evaluation_data["kirkpatrick_level3"] = {
            "observation_window": observation_window,
            "supervisor_feedback": supervisor_feedback,
            "on_the_job_application": "Survey + observation recommended",
            "behavior_trends": [],
        }

        self.evaluation_data["kirkpatrick_level3"]["behavior_trends"].append(
            "Monitor reporting rates and safe behavior adoption across departments."
        )

        return self.evaluation_data["kirkpatrick_level3"]

    def evaluate_results(self):
        """Level 4: Measure business impact"""
        print("\n=== EVALUATE: LEVEL 4 (RESULTS) ===")

        incidents_before = input("Enter number of incidents BEFORE training: ").strip()
        incidents_after = input("Enter number of incidents AFTER training: ").strip()
        training_cost = input("Enter training cost: ").strip()

        try:
            before_val = float(incidents_before)
        except ValueError:
            before_val = 0.0

        try:
            after_val = float(incidents_after)
        except ValueError:
            after_val = 0.0

        try:
            cost_val = float(training_cost)
        except ValueError:
            cost_val = 0.0

        reduction = before_val - after_val
        reduction_percent = (reduction / before_val * 100) if before_val > 0 else 0.0

        assumed_cost_per_incident = 1000.0
        savings = reduction * assumed_cost_per_incident
        roi = ((savings - cost_val) / cost_val * 100) if cost_val > 0 else 0.0

        self.evaluation_data["kirkpatrick_level4"] = {
            "incidents_before": before_val,
            "incidents_after": after_val,
            "incident_reduction": reduction,
            "incident_reduction_percent": reduction_percent,
            "training_cost": cost_val,
            "assumed_cost_per_incident": assumed_cost_per_incident,
            "estimated_savings": savings,
            "estimated_roi_percent": roi,
            "organizational_impact_notes": "",
        }

        self.evaluation_data["kirkpatrick_level4"]["organizational_impact_notes"] = (
            "Track incidents over time and compare to success metrics to validate long-term outcomes."
        )

        return self.evaluation_data["kirkpatrick_level4"]

    def generate_recommendations(self):
        """Generate improvement recommendations"""
        print("\n=== GENERATE RECOMMENDATIONS ===")

        recs = []

        l1 = self.evaluation_data.get("kirkpatrick_level1", {})
        if l1.get("avg_satisfaction_rating", 5) < 4:
            recs.append(
                "Improve training engagement: add more interactive scenarios and clearer pacing."
            )

        l2 = self.evaluation_data.get("kirkpatrick_level2", {})
        if l2.get("post_test_avg_percent", 100) < 80:
            recs.append(
                "Add reinforcement content for weak knowledge areas and provide optional remediation."
            )

        l4 = self.evaluation_data.get("kirkpatrick_level4", {})
        if l4.get("incident_reduction_percent", 100) < 20:
            recs.append(
                "Increase frequency of follow-ups and reinforce behavior change with phishing simulations."
            )

        if not recs:
            recs.append("Maintain current approach and expand content for advanced learners.")

        prioritized = []
        for i, r in enumerate(recs, start=1):
            prioritized.append({"priority": i, "recommendation": r})

        self.evaluation_data["recommendations"] = prioritized
        return prioritized

    def create_evaluation_report(self, output_dir: str = "evaluate"):
        """Generate comprehensive evaluation report"""
        os.makedirs(output_dir, exist_ok=True)

        json_path = f"{output_dir}/evaluate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        txt_path = json_path.replace(".json", ".txt")

        with open(json_path, "w") as f:
            json.dump(self.evaluation_data, f, indent=4)

        with open(txt_path, "w") as f:
            f.write("=== ADDIE EVALUATION REPORT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            f.write("KIRKPATRICK LEVEL 1 (REACTION):\n")
            f.write(json.dumps(self.evaluation_data["kirkpatrick_level1"], indent=4))

            f.write("\n\nKIRKPATRICK LEVEL 2 (LEARNING):\n")
            f.write(json.dumps(self.evaluation_data["kirkpatrick_level2"], indent=4))

            f.write("\n\nKIRKPATRICK LEVEL 3 (BEHAVIOR):\n")
            f.write(json.dumps(self.evaluation_data["kirkpatrick_level3"], indent=4))

            f.write("\n\nKIRKPATRICK LEVEL 4 (RESULTS):\n")
            f.write(json.dumps(self.evaluation_data["kirkpatrick_level4"], indent=4))

            f.write("\n\nRECOMMENDATIONS:\n")
            f.write(json.dumps(self.evaluation_data["recommendations"], indent=4))
            f.write("\n")

        print(f"Evaluation JSON saved to {json_path}")
        print(f"Evaluation text report saved to {txt_path}")

        return json_path, txt_path


if __name__ == "__main__":
    evaluator = EvaluatePhase()
    evaluator.evaluate_reaction()
    evaluator.evaluate_learning()
    evaluator.evaluate_behavior()
    evaluator.evaluate_results()
    evaluator.generate_recommendations()
    evaluator.create_evaluation_report()
