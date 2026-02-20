#!/usr/bin/env python3
"""
Audience Segmentation System for Security Training
Complete implementation version
"""

import csv
import os
from collections import defaultdict


class SecurityTrainingSegmentation:
    def __init__(self, csv_file="employees.csv"):
        """Initialize segmentation system and load employee data."""
        self.employees = []
        self.segments = {}
        self.load_employee_data(csv_file)

    def load_employee_data(self, csv_file):
        """
        Load employee data from CSV file.
        """
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        employees = []
        with open(csv_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to integers
                row["years_experience"] = int(row.get("years_experience", 0))
                row["risk_score"] = int(row.get("risk_score", 0))
                employees.append(row)

        self.employees = employees

    def segment_by_department(self):
        """
        Segment employees by department.
        """
        dept_groups = defaultdict(list)
        for emp in self.employees:
            dept_groups[emp.get("department", "Unknown")].append(emp)

        self.segments["department"] = dict(dept_groups)
        return self.segments["department"]

    def segment_by_risk_level(self):
        """
        Segment employees by risk score into four categories.
        """
        risk_segments = {
            "Low Risk (1-3)": [],
            "Medium Risk (4-6)": [],
            "High Risk (7-9)": [],
            "Critical Risk (10-12)": [],
        }

        for emp in self.employees:
            r = int(emp.get("risk_score", 0))
            if 1 <= r <= 3:
                risk_segments["Low Risk (1-3)"].append(emp)
            elif 4 <= r <= 6:
                risk_segments["Medium Risk (4-6)"].append(emp)
            elif 7 <= r <= 9:
                risk_segments["High Risk (7-9)"].append(emp)
            else:
                risk_segments["Critical Risk (10-12)"].append(emp)

        self.segments["risk"] = risk_segments
        return risk_segments

    def segment_by_training_urgency(self):
        """
        Calculate training urgency based on multiple factors.
        Immediate >= 15
        High >= 10
        Medium >= 6
        Low < 6
        """
        urgency_segments = {
            "Immediate": [],
            "High Priority": [],
            "Medium Priority": [],
            "Low Priority": [],
        }

        def training_points(last_training: str) -> int:
            mapping = {
                "Never": 6,
                "Over 1 year ago": 4,
                "6-12 months ago": 2,
                "Within 3 months": 0,
            }
            return mapping.get(last_training, 3)

        def incident_points(incident_history: str) -> int:
            mapping = {
                "None": 0,
                "Minor": 2,
                "Moderate": 4,
                "Severe": 6,
            }
            return mapping.get(incident_history, 0)

        def access_points(access_level: str) -> int:
            mapping = {
                "Low": 0,
                "Medium": 2,
                "High": 3,
                "Critical": 5,
            }
            return mapping.get(access_level, 2)

        for emp in self.employees:
            risk = int(emp.get("risk_score", 0))
            lt = emp.get("last_training", "Over 1 year ago")
            ih = emp.get("incident_history", "None")
            al = emp.get("access_level", "Medium")

            urgency_score = (
                risk
                + training_points(lt)
                + incident_points(ih)
                + access_points(al)
            )

            emp["urgency_score"] = urgency_score

            if urgency_score >= 15:
                urgency_segments["Immediate"].append(emp)
            elif urgency_score >= 10:
                urgency_segments["High Priority"].append(emp)
            elif urgency_score >= 6:
                urgency_segments["Medium Priority"].append(emp)
            else:
                urgency_segments["Low Priority"].append(emp)

        self.segments["urgency"] = urgency_segments
        return urgency_segments

    def generate_segment_report(self):
        """Generate and print comprehensive segmentation report."""
        total = len(self.employees)

        print("\n=== SECURITY TRAINING SEGMENTATION REPORT ===")
        print(f"Total Employees: {total}\n")

        # Department distribution
        dept_seg = self.segments.get("department", {})
        if dept_seg:
            print("Department Distribution:")
            for dept, emps in sorted(dept_seg.items(), key=lambda x: len(x[1]), reverse=True):
                pct = (len(emps) / total * 100) if total else 0
                print(f"- {dept}: {len(emps)} ({pct:.1f}%)")
            print()

        # Risk distribution
        risk_seg = self.segments.get("risk", {})
        if risk_seg:
            print("Risk Level Distribution:")
            for k, emps in risk_seg.items():
                pct = (len(emps) / total * 100) if total else 0
                print(f"- {k}: {len(emps)} ({pct:.1f}%)")
            print()

        # Urgency distribution
        urg_seg = self.segments.get("urgency", {})
        if urg_seg:
            print("Training Urgency Distribution:")
            for k, emps in urg_seg.items():
                pct = (len(emps) / total * 100) if total else 0
                print(f"- {k}: {len(emps)} ({pct:.1f}%)")
            print()

    def export_segments_to_csv(self):
        """Export each segment to separate CSV files."""
        if not self.segments:
            print("No segments found. Run segmentation methods first.")
            return

        base_fields = list(self.employees[0].keys()) if self.employees else []
        if "urgency_score" not in base_fields:
            base_fields.append("urgency_score")

        for seg_type, seg_data in self.segments.items():
            for name, emps in seg_data.items():
                if not emps:
                    continue

                safe_type = seg_type.replace(" ", "_").lower()
                safe_name = (
                    name.replace(" ", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("/", "_")
                    .lower()
                )

                out_file = f"segment_{safe_type}_{safe_name}.csv"

                with open(out_file, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=base_fields)
                    writer.writeheader()
                    for emp in emps:
                        if "urgency_score" not in emp:
                            emp["urgency_score"] = ""
                        writer.writerow(emp)

        print("Segment CSV exports complete (segment_*.csv created).")


def main():
    seg = SecurityTrainingSegmentation("employees.csv")

    seg.segment_by_department()
    seg.segment_by_risk_level()
    seg.segment_by_training_urgency()

    seg.generate_segment_report()
    seg.export_segments_to_csv()


if __name__ == "__main__":
    main()
