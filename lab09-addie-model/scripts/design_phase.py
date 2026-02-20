#!/usr/bin/env python3
"""
ADDIE Design Phase Implementation
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class DesignPhase:
    def __init__(self, analysis_data: Dict = None):
        self.analysis_data = analysis_data if analysis_data else {}
        self.design_data = {
            "learning_objectives": [],
            "assessment_strategy": {},
            "instructional_strategy": {},
            "content_outline": {},
            "delivery_method": {},
        }

    def create_learning_objectives(self):
        """
        Create SMART learning objectives based on analysis
        SMART: Specific, Measurable, Achievable, Relevant, Time-bound
        """
        print("\n=== LEARNING OBJECTIVES ===")

        goals = []
        if "goals" in self.analysis_data and "learning_goals" in self.analysis_data["goals"]:
            goals = self.analysis_data["goals"]["learning_goals"]

        if not goals:
            goals = input("No analysis goals found. Enter learning goals (comma separated): ").split(",")
            goals = [g.strip() for g in goals if g.strip()]

        objectives: List[Dict] = []
        for idx, g in enumerate(goals, start=1):
            objective = {
                "id": f"OBJ{idx:02d}",
                "objective": f"By the end of this training, learners will be able to {g.lower()}",
                "bloom_level": "Apply",
                "assessment_method": "Quiz + Scenario Exercise",
                "estimated_minutes": 20,
                "smart_check": {
                    "specific": True,
                    "measurable": True,
                    "achievable": True,
                    "relevant": True,
                    "time_bound": True,
                },
            }
            objectives.append(objective)

        self.design_data["learning_objectives"] = objectives
        return objectives

    def design_assessment_strategy(self):
        """Design comprehensive assessment approach"""
        print("\n=== ASSESSMENT STRATEGY ===")

        strategy = {
            "types": {
                "pre_assessment": "Baseline quiz (10 questions)",
                "formative": "Module mini-quizzes + interactive checks",
                "summative": "Final exam (25 questions) + scenario assessment",
            },
            "passing_criteria": {
                "final_exam_min_score_percent": 80,
                "scenario_required": True
            },
            "tools": [
                "LMS quiz engine",
                "Google Forms/Equivalent",
                "Scenario simulations"
            ],
            "feedback": {
                "immediate_feedback": True,
                "explanations_provided": True,
                "remediation_path": "Extra practice + retake allowed once",
            },
        }

        self.design_data["assessment_strategy"] = strategy
        return strategy

    def design_instructional_strategy(self):
        """Design instructional approach and methods"""
        print("\n=== INSTRUCTIONAL STRATEGY ===")

        learner_prefs = None
        if (
            "learner_analysis" in self.analysis_data
            and "preferences" in self.analysis_data["learner_analysis"]
        ):
            learner_prefs = self.analysis_data["learner_analysis"]["preferences"]

        strategy = {
            "learning_theory": "Cognitivism + Constructivism (scenario-based learning)",
            "methods": [
                "Microlearning",
                "Interactive scenarios",
                "Demonstrations",
                "Knowledge checks"
            ],
            "engagement": [
                "Gamified badges",
                "Real-world examples",
                "Peer discussion prompts"
            ],
            "alignment_with_preferences": learner_prefs if learner_prefs else "Not provided in analysis",
        }

        self.design_data["instructional_strategy"] = strategy
        return strategy

    def create_content_outline(self):
        """Create detailed content structure"""
        print("\n=== CONTENT OUTLINE ===")

        objectives = self.design_data.get("learning_objectives", [])
        if not objectives:
            self.create_learning_objectives()

        modules = {
            "Module 1": {
                "title": "Introduction to Security Awareness",
                "topics": [
                    "Why security matters",
                    "Threat landscape basics",
                    "User responsibility"
                ],
                "activities": [
                    "Short video",
                    "Quick quiz",
                    "Discussion prompt"
                ],
                "estimated_minutes": 30,
            },
            "Module 2": {
                "title": "Phishing and Social Engineering",
                "topics": [
                    "Email phishing",
                    "Spear phishing",
                    "Social engineering tactics"
                ],
                "activities": [
                    "Scenario simulation",
                    "Spot-the-phish exercise"
                ],
                "estimated_minutes": 45,
            },
            "Module 3": {
                "title": "Passwords and Authentication",
                "topics": [
                    "Password best practices",
                    "MFA",
                    "Password managers"
                ],
                "activities": [
                    "Password strength exercise",
                    "Hands-on MFA walkthrough"
                ],
                "estimated_minutes": 35,
            },
            "Module 4": {
                "title": "Incident Reporting and Safe Practices",
                "topics": [
                    "How to report",
                    "Device hygiene",
                    "Safe browsing and handling data"
                ],
                "activities": [
                    "Incident reporting drill",
                    "Checklist assignment"
                ],
                "estimated_minutes": 30,
            },
        }

        self.design_data["content_outline"] = {
            "modules": modules,
            "objective_alignment": [o["id"] for o in objectives],
        }

        return self.design_data["content_outline"]

    def design_delivery_method(self):
        """Design delivery logistics and requirements"""
        print("\n=== DELIVERY METHOD ===")

        delivery = {
            "format": "Online",
            "platform": "LMS (or equivalent)",
            "tools": [
                "Video conferencing (optional)",
                "LMS",
                "Email notifications"
            ],
            "technical_requirements": [
                "Modern browser",
                "Audio support",
                "Stable internet"
            ],
            "support_resources": [
                "FAQ page",
                "Help desk email",
                "Instructor office hours"
            ],
        }

        self.design_data["delivery_method"] = delivery
        return delivery

    def generate_design_document(self, output_dir: str = "design"):
        """
        Generate comprehensive design document
        """
        os.makedirs(output_dir, exist_ok=True)

        json_path = f"{output_dir}/design_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        txt_path = json_path.replace(".json", ".txt")

        with open(json_path, "w") as f:
            json.dump(self.design_data, f, indent=4)

        with open(txt_path, "w") as f:
            f.write("=== ADDIE DESIGN DOCUMENT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            f.write("LEARNING OBJECTIVES:\n")
            for obj in self.design_data["learning_objectives"]:
                f.write(f"- {obj['id']}: {obj['objective']} (Bloom: {obj['bloom_level']})\n")
                f.write(f"  Assessment: {obj['assessment_method']}, Time: {obj['estimated_minutes']} mins\n")

            f.write("\nASSESSMENT STRATEGY:\n")
            f.write(json.dumps(self.design_data["assessment_strategy"], indent=4))

            f.write("\n\nINSTRUCTIONAL STRATEGY:\n")
            f.write(json.dumps(self.design_data["instructional_strategy"], indent=4))

            f.write("\n\nCONTENT OUTLINE:\n")
            f.write(json.dumps(self.design_data["content_outline"], indent=4))

            f.write("\n\nDELIVERY METHOD:\n")
            f.write(json.dumps(self.design_data["delivery_method"], indent=4))
            f.write("\n")

        print(f"Design JSON saved to {json_path}")
        print(f"Design text document saved to {txt_path}")

        return json_path, txt_path


if __name__ == "__main__":
    designer = DesignPhase()
    designer.create_learning_objectives()
    designer.design_assessment_strategy()
    designer.design_instructional_strategy()
    designer.create_content_outline()
    designer.design_delivery_method()
    designer.generate_design_document()
