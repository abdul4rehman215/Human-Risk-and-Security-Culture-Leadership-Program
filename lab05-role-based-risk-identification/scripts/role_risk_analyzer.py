#!/usr/bin/env python3
"""
Role-Based Risk Identification Tool
Students: Complete the TODO sections
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any


class RoleRiskAnalyzer:
    def __init__(self):
        self.roles_data: Dict[str, Any] = {}
        self.cti_data: Dict[str, Any] = {}
        self.risk_scores: Dict[str, Any] = {}

    def load_organizational_data(self, roles_file):
        """
        Load organizational role data from JSON file.

        Args:
            roles_file: Path to roles JSON file

        Returns:
            Boolean indicating success
        """
        try:
            # Open and load the JSON file
            with open(roles_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Store data in self.roles_data
            self.roles_data = data

            # Print success message with role count
            print(f"[INFO] Loaded organizational roles: {len(self.roles_data)} roles")

            # Return True on success
            return True

        except FileNotFoundError:
            print(f"[ERROR] File {roles_file} not found")
            return False
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format")
            return False

    def load_cti_data(self, cti_file):
        """
        Load Cyber Threat Intelligence data.

        Args:
            cti_file: Path to CTI JSON file

        Returns:
            Boolean indicating success
        """
        try:
            with open(cti_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.cti_data = data
            print(f"[INFO] Loaded CTI data categories: {len(self.cti_data)} categories")
            return True

        except FileNotFoundError:
            print(f"[ERROR] File {cti_file} not found")
            return False
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format in CTI file")
            return False

    def calculate_base_risk_score(self, role_info):
        """
        Calculate base risk score for a role.

        Formula:
        (access_level * 0.3 +
         data_sensitivity * 0.25 +
         external_exposure * 0.25 +
         privilege_level * 0.2) * 10

        Returns:
            Float: Base risk score (0-100)
        """
        access_level = float(role_info.get("access_level", 0))
        data_sensitivity = float(role_info.get("data_sensitivity", 0))
        external_exposure = float(role_info.get("external_exposure", 0))
        privilege_level = float(role_info.get("privilege_level", 0))

        score = (
            access_level * 0.3
            + data_sensitivity * 0.25
            + external_exposure * 0.25
            + privilege_level * 0.2
        ) * 10.0

        return round(score, 2)

    def apply_cti_modifiers(self, base_score, role_type):
        """
        Apply CTI-based risk modifiers to base score.
        """
        if not self.cti_data:
            return base_score

        modifier = 1.0

        for category_name, threats in self.cti_data.items():
            if not isinstance(threats, list):
                continue

            for threat in threats:
                target_roles = threat.get("target_roles", [])
                severity = float(threat.get("severity", 0))

                if role_type in target_roles:
                    modifier += severity * 0.1

        modified_score = base_score * modifier

        if modified_score > 100:
            modified_score = 100.0

        return round(modified_score, 2)

    def classify_risk_level(self, score):
        """
        Classify risk level based on score.
        """
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"

    def analyze_all_roles(self):
        """
        Analyze risk for all loaded roles.
        """
        if not self.roles_data:
            print("[ERROR] No role data loaded")
            return False

        print("\n[INFO] Starting role-based risk analysis...")

        self.risk_scores = {}

        for role_id, info in self.roles_data.items():
            role_name = info.get("name", "Unknown")
            role_type = info.get("type", "unknown")
            department = info.get("department", "Unknown")

            base_score = self.calculate_base_risk_score(info)
            final_score = self.apply_cti_modifiers(base_score, role_type)
            risk_level = self.classify_risk_level(final_score)

            self.risk_scores[role_id] = {
                "role_name": role_name,
                "role_type": role_type,
                "department": department,
                "base_score": base_score,
                "final_score": final_score,
                "risk_level": risk_level,
                "analyzed_at": datetime.now().isoformat(),
                "raw_attributes": info,
            }

        print(f"[INFO] Risk analysis complete. Roles analyzed: {len(self.risk_scores)}")
        return True

    def generate_risk_report(self, output_file="risk_report.json"):
        """
        Generate comprehensive risk report.
        """
        if not self.risk_scores:
            print("[ERROR] No risk analysis data available")
            return False

        scores = [v["final_score"] for v in self.risk_scores.values()]
        avg_score = round(float(np.mean(scores)), 2) if scores else 0.0
        min_score = round(float(np.min(scores)), 2) if scores else 0.0
        max_score = round(float(np.max(scores)), 2) if scores else 0.0

        risk_dist = {}
        for v in self.risk_scores.values():
            lvl = v["risk_level"]
            risk_dist[lvl] = risk_dist.get(lvl, 0) + 1

        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_roles": len(self.risk_scores),
                "average_score": avg_score,
                "min_score": min_score,
                "max_score": max_score,
                "risk_level_distribution": risk_dist,
            },
            "detailed_analysis": self.risk_scores,
        }

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"[INFO] Risk report saved to {output_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save report: {e}")
            return False

    def display_top_risks(self, top_n=10):
        """
        Display top N highest risk roles.
        """
        if not self.risk_scores:
            print("[ERROR] No risk analysis data available")
            return

        sorted_roles = sorted(
            self.risk_scores.items(),
            key=lambda x: x[1]["final_score"],
            reverse=True
        )

        print("\nTop Risk Roles")
        print("=" * 70)
        print(f"{'Rank':<6}{'Role Name':<30}{'Department':<20}{'Score':<8}{'Level':<10}")
        print("-" * 70)

        for idx, (role_id, info) in enumerate(sorted_roles[:top_n], start=1):
            print(
                f"{idx:<6}{info['role_name']:<30}"
                f"{info['department']:<20}"
                f"{info['final_score']:<8}"
                f"{info['risk_level']:<10}"
            )

        print("-" * 70)


if __name__ == "__main__":
    print("Role-Based Risk Identification Tool")
    print("=" * 50)
    analyzer = RoleRiskAnalyzer()
    print("\nTool initialized. Ready for analysis.")
