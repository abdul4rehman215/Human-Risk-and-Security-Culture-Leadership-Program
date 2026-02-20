#!/usr/bin/env python3
"""
Project Planning Engine
Full Implementation
Creates detailed project plans for long-term security programs
"""

import json
import datetime
import pandas as pd
from pathlib import Path


class ProjectPlanner:
    def __init__(self, strategy_path):
        self.strategy = self.load_strategy(strategy_path)

    def load_strategy(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Strategy report not found. Run strategy_engine.py first.")
            exit(1)
        except json.JSONDecodeError:
            print("Strategy report JSON is invalid.")
            exit(1)

    def create_task_breakdown(self):
        """
        Break down phases into detailed tasks and subtasks.
        Returns list of tasks with start/end dates and durations.
        """
        phases = self.strategy["roadmap"]["phases"]
        start_date = datetime.datetime.strptime(
            self.strategy["timeline"]["start_date"], "%Y-%m-%d"
        )

        task_list = []
        current_start = start_date
        task_id = 1

        phase_task_templates = {
            "Foundation": [
                ("Baseline Assessment",
                 ["Survey security culture",
                  "Review incidents data",
                  "Assess awareness maturity"]),
                ("Policy Development",
                 ["Review existing policies",
                  "Update policies",
                  "Publish policies"]),
                ("Initial Training Rollout",
                 ["Create training content",
                  "Launch training campaign",
                  "Collect feedback"])
            ],
            "Implementation": [
                ("Program Rollout",
                 ["Deploy training portal",
                  "Communicate program",
                  "Start monthly campaigns"]),
                ("Training Delivery",
                 ["Run sessions",
                  "Track completions",
                  "Run phishing simulations"]),
                ("Culture Change Activities",
                 ["Ambassador program",
                  "Gamification",
                  "Monthly security tips"])
            ],
            "Optimization": [
                ("Continuous Improvement",
                 ["Analyze metrics",
                  "Update content",
                  "Improve delivery"]),
                ("Advanced Training",
                 ["Role-based training",
                  "Executive training",
                  "High-risk user drills"]),
                ("Sustainability",
                 ["Transfer ownership",
                  "Embed KPIs",
                  "Establish recurring reviews"])
            ]
        }

        for phase in phases:
            phase_name = phase["name"]
            duration_months = phase["duration_months"]

            phase_end = current_start + datetime.timedelta(days=duration_months * 30)

            templates = phase_task_templates.get(phase_name, [])
            if not templates:
                templates = [(f"{phase_name} General Task",
                              ["Subtask 1", "Subtask 2", "Subtask 3"])]

            main_task_days = max(
                1,
                int((phase_end - current_start).days /
                    max(1, len(templates)))
            )

            for main_task, subtasks in templates:
                main_start = current_start
                main_end = main_start + datetime.timedelta(days=main_task_days)

                task_list.append({
                    "task_id": f"T{task_id:04d}",
                    "phase": phase_name,
                    "task_name": main_task,
                    "task_type": "main",
                    "start_date": main_start.strftime("%Y-%m-%d"),
                    "end_date": main_end.strftime("%Y-%m-%d"),
                    "duration_days": (main_end - main_start).days
                })
                parent_id = f"T{task_id:04d}"
                task_id += 1

                subtask_days = max(
                    1,
                    int((main_end - main_start).days /
                        max(1, len(subtasks)))
                )

                sub_current = main_start

                for st in subtasks:
                    st_start = sub_current
                    st_end = st_start + datetime.timedelta(days=subtask_days)

                    if st_end > main_end:
                        st_end = main_end

                    task_list.append({
                        "task_id": f"T{task_id:04d}",
                        "parent_task_id": parent_id,
                        "phase": phase_name,
                        "task_name": st,
                        "task_type": "subtask",
                        "start_date": st_start.strftime("%Y-%m-%d"),
                        "end_date": st_end.strftime("%Y-%m-%d"),
                        "duration_days": (st_end - st_start).days
                    })
                    task_id += 1
                    sub_current = st_end

                current_start = main_end

            if current_start < phase_end:
                current_start = phase_end

        return task_list

    def generate_milestones(self):
        milestones = []
        timeline = self.strategy["timeline"]
        phases = self.strategy["roadmap"]["phases"]

        start_date = datetime.datetime.strptime(
            timeline["start_date"], "%Y-%m-%d"
        )
        current = start_date

        for phase in phases:
            phase_end = current + datetime.timedelta(days=phase["duration_months"] * 30)
            milestones.append({
                "milestone_name": f"{phase['name']} Phase Completed",
                "date": phase_end.strftime("%Y-%m-%d"),
                "success_criteria": [
                    "All deliverables completed",
                    "KPIs trending toward targets",
                    "Stakeholder review completed"
                ]
            })
            current = phase_end

        for m_date in timeline["quarterly_milestones"]:
            milestones.append({
                "milestone_name": "Quarterly Program Review",
                "date": m_date,
                "success_criteria": [
                    "Quarterly metrics report delivered",
                    "Risks reviewed and mitigations updated",
                    "Next quarter priorities confirmed"
                ]
            })

        milestones.sort(key=lambda x: x["date"])
        return milestones

    def create_resource_plan(self):
        resource_plan = {
            "roles": [
                {"role": "Program Manager", "allocation": "0.5 FTE",
                 "responsibilities": ["Planning", "Reporting", "Stakeholder management"]},
                {"role": "Security Awareness Lead", "allocation": "1.0 FTE",
                 "responsibilities": ["Content creation", "Campaigns", "Training delivery"]},
                {"role": "Security Analyst", "allocation": "0.5 FTE",
                 "responsibilities": ["Metrics tracking", "Phishing simulations", "Incident analysis"]},
                {"role": "HR Partner", "allocation": "0.2 FTE",
                 "responsibilities": ["Employee comms", "Training coordination"]},
                {"role": "IT Support", "allocation": "0.2 FTE",
                 "responsibilities": ["Platform support", "Tool integrations"]}
            ],
            "budget_estimates": {
                "training_platform": 25000,
                "content_development": 15000,
                "phishing_simulation_tools": 12000,
                "incentives_rewards": 8000,
                "consulting_support": 20000
            }
        }
        return resource_plan

    def identify_risks(self):
        risks = [
            {
                "risk": "Low employee participation",
                "probability": "High",
                "impact": "High",
                "mitigation": [
                    "Executive sponsorship",
                    "Gamification",
                    "Short role-based training"
                ]
            },
            {
                "risk": "Budget constraints",
                "probability": "Medium",
                "impact": "High",
                "mitigation": [
                    "Prioritize high-impact activities",
                    "Use open-source tools",
                    "Phase investments"
                ]
            }
        ]
        return {"risks": risks}

    def generate_project_plan(self):
        task_list = self.create_task_breakdown()
        milestones = self.generate_milestones()
        resources = self.create_resource_plan()
        risks = self.identify_risks()

        plan = {
            "metadata": {
                "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_strategy": "strategy_report.json"
            },
            "program_timeline": self.strategy["timeline"],
            "tasks": task_list,
            "milestones": milestones,
            "resource_plan": resources,
            "risk_management": risks
        }

        return plan

    def export_task_csv(self, plan, filename):
        tasks = plan["tasks"]
        df = pd.DataFrame(tasks)
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"Task list exported to {filename}")


def main():
    print("=== Project Planning Engine ===")

    planner = ProjectPlanner("reports/strategy_report.json")
    plan = planner.generate_project_plan()

    Path("reports").mkdir(exist_ok=True)
    with open("reports/project_plan.json", "w") as f:
        json.dump(plan, f, indent=4)

    planner.export_task_csv(plan, "data/task_list.csv")

    print("Project plan saved to reports/project_plan.json")
    print("Total tasks:", len(plan["tasks"]))
    print("Total milestones:", len(plan["milestones"]))


if __name__ == "__main__":
    main()
