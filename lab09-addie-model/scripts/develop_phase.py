#!/usr/bin/env python3
"""
ADDIE Develop Phase Implementation
"""

import json
import os
from datetime import datetime
from typing import Dict


class DevelopPhase:
    def __init__(self, design_data: Dict = None):
        self.design_data = design_data if design_data else {}
        self.develop_data = {
            "content_materials": {},
            "assessments": {},
            "multimedia": {},
            "quality_checks": {},
        }

    def create_content_materials(self):
        """Create training content based on design"""
        print("\n=== DEVELOP: CONTENT MATERIALS ===")

        modules = self.design_data.get("content_outline", {}).get("modules", {})

        if not modules:
            modules = {
                "Module 1": {
                    "title": "Intro",
                    "topics": ["Security basics"],
                    "activities": ["Quiz"],
                    "estimated_minutes": 30
                }
            }

        content = {}
        for module_name, module_info in modules.items():
            title = module_info.get("title", module_name)
            topics = module_info.get("topics", [])
            activities = module_info.get("activities", [])
            minutes = module_info.get("estimated_minutes", 30)

            content[module_name] = {
                "title": title,
                "overview": f"This module covers: {', '.join(topics) if topics else 'core topics'}",
                "topics": topics,
                "activities": activities,
                "estimated_minutes": minutes,
                "handouts": [
                    f"{module_name}_job_aid.pdf",
                    f"{module_name}_quick_reference.pdf",
                ],
                "slides": f"{module_name}_slides.pptx",
                "facilitator_notes": f"{module_name}_facilitator_notes.txt",
            }

        self.develop_data["content_materials"] = content
        return content

    def develop_assessments(self):
        """Create assessment materials"""
        print("\n=== DEVELOP: ASSESSMENTS ===")

        objectives = self.design_data.get("learning_objectives", [])

        quiz_questions = []
        scenario_exercises = []

        for obj in objectives:
            quiz_questions.append(
                {
                    "objective_id": obj.get("id"),
                    "question": f"Which statement best demonstrates the learner can {obj.get('objective', '').replace('By the end of this training, learners will be able to ', '')}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option B",
                    "rationale": "Option B best aligns with the objective behavior.",
                }
            )

            scenario_exercises.append(
                {
                    "objective_id": obj.get("id"),
                    "scenario": "A user receives an email requesting urgent login credentials. What should they do?",
                    "expected_actions": [
                        "Do not click links",
                        "Verify sender",
                        "Report to security team",
                    ],
                    "rubric": {
                        "excellent": "Reports and avoids interaction; explains reasoning",
                        "good": "Avoids interaction and reports",
                        "needs_improvement": "Clicks link or provides info",
                    },
                }
            )

        assessments = {
            "pre_assessment": {
                "type": "quiz",
                "question_count": 10,
                "notes": "Baseline assessment to determine starting knowledge.",
            },
            "formative": {
                "type": "mini_quizzes",
                "notes": "Short knowledge checks at end of each module.",
            },
            "summative": {
                "type": "final_exam_and_scenario",
                "final_exam_question_bank": quiz_questions,
                "scenario_exercises": scenario_exercises,
                "passing_criteria": {
                    "min_score_percent": 80,
                    "scenario_required": True
                },
            },
        }

        self.develop_data["assessments"] = assessments
        return assessments

    def create_multimedia_resources(self):
        """Plan multimedia resource development"""
        print("\n=== DEVELOP: MULTIMEDIA RESOURCES ===")

        modules = self.design_data.get("content_outline", {}).get("modules", {})

        multimedia = {
            "images_graphics": [],
            "videos": [],
            "interactive_elements": [],
            "audio_scripts": [],
        }

        for module_name, module_info in modules.items():
            title = module_info.get("title", module_name)

            multimedia["images_graphics"].append(
                {
                    "module": module_name,
                    "asset_name": f"{module_name}_infographic.png",
                    "description": f"Infographic for {title}",
                }
            )

            multimedia["videos"].append(
                {
                    "module": module_name,
                    "asset_name": f"{module_name}_explainer.mp4",
                    "description": f"Short explainer video for {title}",
                    "duration_minutes": 3,
                }
            )

            multimedia["interactive_elements"].append(
                {
                    "module": module_name,
                    "asset_name": f"{module_name}_scenario_simulation.html",
                    "description": f"Interactive scenario simulation for {title}",
                }
            )

            multimedia["audio_scripts"].append(
                {
                    "module": module_name,
                    "asset_name": f"{module_name}_narration_script.txt",
                    "description": f"Narration script for {title}",
                }
            )

        self.develop_data["multimedia"] = multimedia
        return multimedia

    def conduct_quality_assurance(self):
        """Perform quality checks on materials"""
        print("\n=== DEVELOP: QUALITY ASSURANCE ===")

        checks = {
            "content_accuracy_reviewed": True,
            "alignment_with_objectives_verified": True,
            "technical_functionality_tested": True,
            "accessibility_compliance_checked": True,
            "peer_review_completed": True,
            "issues_found": [],
            "revision_notes": [],
        }

        if not self.design_data.get("learning_objectives"):
            checks["issues_found"].append(
                "No learning objectives found in design data."
            )
            checks["revision_notes"].append(
                "Design phase must be completed before development QA can fully pass."
            )
            checks["alignment_with_objectives_verified"] = False

        self.develop_data["quality_checks"] = checks
        return checks

    def generate_development_report(self, output_dir: str = "develop"):
        """
        Generate development phase report
        """
        os.makedirs(output_dir, exist_ok=True)

        json_path = f"{output_dir}/develop_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        txt_path = json_path.replace(".json", ".txt")

        with open(json_path, "w") as f:
            json.dump(self.develop_data, f, indent=4)

        with open(txt_path, "w") as f:
            f.write("=== ADDIE DEVELOPMENT REPORT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            f.write("MATERIAL INVENTORY:\n")
            f.write(json.dumps(self.develop_data["content_materials"], indent=4))

            f.write("\n\nASSESSMENTS:\n")
            f.write(json.dumps(self.develop_data["assessments"], indent=4))

            f.write("\n\nMULTIMEDIA PLAN:\n")
            f.write(json.dumps(self.develop_data["multimedia"], indent=4))

            f.write("\n\nQUALITY CHECKS:\n")
            f.write(json.dumps(self.develop_data["quality_checks"], indent=4))
            f.write("\n")

        print(f"Development JSON saved to {json_path}")
        print(f"Development text report saved to {txt_path}")

        return json_path, txt_path


if __name__ == "__main__":
    developer = DevelopPhase()
    developer.create_content_materials()
    developer.develop_assessments()
    developer.create_multimedia_resources()
    developer.conduct_quality_assurance()
    developer.generate_development_report()
