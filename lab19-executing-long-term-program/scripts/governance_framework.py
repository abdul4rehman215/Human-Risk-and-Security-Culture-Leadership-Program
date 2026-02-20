#!/usr/bin/env python3
"""
Governance Framework
Full Implementation
Creates governance structure for program sustainability
"""

import json
import datetime
import os


class GovernanceFramework:
    def __init__(self, program_config):
        self.config = program_config

    def define_governance_structure(self):
        """
        Create organizational governance structure.
        """
        structure = {
            "steering_committee": {
                "purpose": "Strategic oversight and executive decision-making",
                "members": [
                    "CISO (Chair)",
                    "HR Head",
                    "IT Director",
                    "Compliance Officer",
                    "Business Unit Representative"
                ],
                "meeting_frequency": "Monthly",
                "responsibilities": [
                    "Approve strategy and budgets",
                    "Review KPI progress quarterly",
                    "Resolve escalations and blockers"
                ]
            },
            "project_board": {
                "purpose": "Tactical execution and cross-functional alignment",
                "members": [
                    "Program Manager",
                    "Security Awareness Lead",
                    "IT Support Lead",
                    "HR Partner"
                ],
                "meeting_frequency": "Bi-weekly",
                "responsibilities": [
                    "Track plan execution",
                    "Coordinate deliverables and tasks",
                    "Manage risks and dependencies"
                ]
            },
            "working_groups": [
                {
                    "group": "Training & Content",
                    "members": [
                        "Security Awareness Lead",
                        "Subject Matter Experts (SMEs)",
                        "HR Partner"
                    ],
                    "focus": "Training content development and awareness campaigns"
                },
                {
                    "group": "Metrics & Reporting",
                    "members": [
                        "Security Analyst",
                        "Program Manager"
                    ],
                    "focus": "KPI collection, dashboards, reporting automation"
                },
                {
                    "group": "Technology & Tools",
                    "members": [
                        "IT Support",
                        "Security Engineer"
                    ],
                    "focus": "Tool integrations, platforms, and technical enablement"
                }
            ],
            "escalation_path": [
                "Working Group → Project Board → Steering Committee"
            ]
        }

        return structure

    def create_decision_framework(self):
        """
        Establish decision-making processes.
        """
        decision = {
            "decision_types": {
                "strategic": {
                    "examples": [
                        "Budget increases",
                        "Major scope change",
                        "Program redesign"
                    ],
                    "authority": "Steering Committee",
                    "approval": "Majority vote with CISO final approval"
                },
                "tactical": {
                    "examples": [
                        "Campaign schedule changes",
                        "Tool configuration updates"
                    ],
                    "authority": "Project Board",
                    "approval": "Program Manager + Awareness Lead approval"
                },
                "operational": {
                    "examples": [
                        "Weekly communications",
                        "Training session scheduling"
                    ],
                    "authority": "Working Groups",
                    "approval": "Working group lead approval"
                }
            },
            "documentation_process": [
                "Log decision in decision_register.json",
                "Include decision, reason, impact, approver, date",
                "Communicate to stakeholders"
            ]
        }

        return decision

    def establish_communication_plan(self):
        """
        Define communication strategy and cadence.
        """
        plan = {
            "stakeholders": {
                "executives": {
                    "channels": [
                        "Monthly executive summary",
                        "Quarterly board review presentation"
                    ],
                    "frequency": "Monthly / Quarterly"
                },
                "managers": {
                    "channels": [
                        "Bi-weekly updates",
                        "Department scorecards"
                    ],
                    "frequency": "Bi-weekly"
                },
                "employees": {
                    "channels": [
                        "Weekly security tips",
                        "Monthly newsletters",
                        "Campaign announcements"
                    ],
                    "frequency": "Weekly / Monthly"
                }
            },
            "communication_templates": {
                "executive_summary": "Focus on ROI, risk reduction, KPI trends, and action items",
                "department_scorecard": "Department performance against awareness, training, and compliance targets",
                "weekly_tip": "Short practical security advice with one actionable takeaway"
            }
        }

        return plan

    def create_sustainability_plan(self):
        """
        Develop long-term sustainability model.
        """
        sustain = {
            "core_requirements": [
                "Continuous measurement of KPIs",
                "Ongoing awareness campaigns",
                "Embedded onboarding training",
                "Annual content refresh cycle"
            ],
            "self_sustaining_processes": [
                "Quarterly review cycle with steering committee",
                "Automated reporting system",
                "Security ambassador program"
            ],
            "knowledge_transfer": {
                "documentation_requirements": [
                    "Maintain runbooks for training and tooling",
                    "Maintain KPI definitions and dashboard documentation"
                ],
                "handover_plan": "Transfer operational ownership to Security Awareness Lead within final 6 months"
            },
            "continuous_improvement_cycle": {
                "model": "Plan → Execute → Measure → Improve",
                "review_frequency": "Quarterly",
                "data_inputs": [
                    "metrics_history.csv",
                    "incident logs",
                    "employee feedback surveys"
                ]
            }
        }

        return sustain

    def generate_governance_document(self):
        """
        Generate complete governance framework document.
        """
        doc = {
            "metadata": {
                "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0",
                "program_name": self.config["program_info"]["name"]
            },
            "governance_structure": self.define_governance_structure(),
            "decision_framework": self.create_decision_framework(),
            "communication_plan": self.establish_communication_plan(),
            "sustainability_plan": self.create_sustainability_plan(),
            "approval_workflow": {
                "prepared_by": "Program Manager",
                "reviewed_by": "Steering Committee",
                "approved_by": "CISO",
                "approval_date": "TBD"
            }
        }

        return doc


def main():
    print("=== Governance Framework Development ===")

    try:
        with open("config/program_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Missing config/program_config.json. Create it first.")
        exit(1)
    except json.JSONDecodeError:
        print("program_config.json is not valid JSON.")
        exit(1)

    governance = GovernanceFramework(config)
    document = governance.generate_governance_document()

    os.makedirs("reports", exist_ok=True)
    with open("reports/governance_framework.json", "w") as f:
        json.dump(document, f, indent=4)

    print("Governance framework saved to reports/governance_framework.json")
    print("Program:", document["metadata"]["program_name"])
    print("Version:", document["metadata"]["version"])


if __name__ == "__main__":
    main()
