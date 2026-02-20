#!/usr/bin/env python3
"""
Security Program Strategy Engine
Full Implementation
"""

import json
import datetime
from pathlib import Path


class SecurityStrategy:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Configuration file not found.")
            exit(1)
        except json.JSONDecodeError:
            print("Invalid JSON format in configuration file.")
            exit(1)

    def calculate_timeline(self):
        program_info = self.config["program_info"]

        start_date = datetime.datetime.strptime(
            program_info["start_date"], "%Y-%m-%d"
        )

        duration_years = program_info["duration_years"]
        end_date = start_date + datetime.timedelta(days=duration_years * 365)

        milestones = []
        current = start_date
        while current < end_date:
            milestones.append(current.strftime("%Y-%m-%d"))
            current += datetime.timedelta(days=90)

        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "quarterly_milestones": milestones
        }

    def generate_roadmap(self):
        roadmap = {
            "phases": [],
            "objectives_progression": {}
        }

        objectives = self.config["objectives"]

        for phase in self.config["phases"]:
            deliverables = [
                f"Complete {focus}" for focus in phase["focus"]
            ]

            roadmap["phases"].append({
                "name": phase["name"],
                "duration_months": phase["duration_months"],
                "focus_areas": phase["focus"],
                "deliverables": deliverables
            })

        for obj_name, values in objectives.items():
            improvement = values["target"] - values["baseline"]
            roadmap["objectives_progression"][obj_name] = {
                "baseline": values["baseline"],
                "target": values["target"],
                "total_improvement_required": improvement
            }

        return roadmap

    def create_kpi_framework(self):
        kpis = {}

        for obj_name, values in self.config["objectives"].items():
            kpis[obj_name] = {
                "baseline": values["baseline"],
                "target": values["target"],
                "measurement_frequency": "Quarterly",
                "status_indicator": "Green >= target, Yellow within 10%, Red below"
            }

        return kpis

    def generate_report(self):
        report = {
            "metadata": {
                "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            },
            "timeline": self.calculate_timeline(),
            "roadmap": self.generate_roadmap(),
            "kpi_framework": self.create_kpi_framework()
        }

        return report

    def save_report(self, report, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        print(f"Strategy report saved to {filename}")


def main():
    print("=== Security Program Strategy Development ===")

    strategy = SecurityStrategy("../config/program_config.json")
    report = strategy.generate_report()
    strategy.save_report(report, "../reports/strategy_report.json")

    print("Program duration:",
          report["timeline"]["start_date"],
          "to",
          report["timeline"]["end_date"])

    print("Total phases:",
          len(report["roadmap"]["phases"]))


if __name__ == "__main__":
    main()
