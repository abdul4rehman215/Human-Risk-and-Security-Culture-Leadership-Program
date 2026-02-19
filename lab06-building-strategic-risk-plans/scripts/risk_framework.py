#!/usr/bin/env python3
"""
Strategic Risk Management Framework
Students will complete this module to align risks, behaviors, and culture
"""

import json
import pandas as pd
from datetime import datetime


class RiskBehaviorCultureFramework:
    def __init__(self):
        # Risk categories with severity levels
        self.risk_categories = {
            "phishing": {"severity": "high", "frequency": "daily"},
            "weak_passwords": {"severity": "medium", "frequency": "continuous"},
            "social_engineering": {"severity": "high", "frequency": "weekly"},
            "insider_threats": {"severity": "critical", "frequency": "monthly"},
            "unsecured_devices": {"severity": "medium", "frequency": "daily"},
        }

        # Behavioral pattern multipliers
        self.behavioral_patterns = {
            "security_awareness": {
                "low": {"risk_multiplier": 2.5},
                "medium": {"risk_multiplier": 1.5},
                "high": {"risk_multiplier": 0.8},
            },
            "compliance_adherence": {
                "low": {"risk_multiplier": 2.0},
                "medium": {"risk_multiplier": 1.3},
                "high": {"risk_multiplier": 0.7},
            },
        }

        # Culture factors and weights
        self.culture_factors = {
            "leadership_commitment": {"weight": 0.3},
            "employee_engagement": {"weight": 0.25},
            "communication_effectiveness": {"weight": 0.2},
            "learning_culture": {"weight": 0.15},
            "accountability_structure": {"weight": 0.1},
        }

    def calculate_risk_score(self, risk_type, behavior_level, culture_score):
        """
        Calculate comprehensive risk score based on risk, behavior, and culture.

        Args:
            risk_type: Type of risk from risk_categories
            behavior_level: 'low', 'medium', or 'high'
            culture_score: Float between 0.0 and 1.0

        Returns:
            Float risk score (0-10 scale)
        """

        severity_map = {
            "critical": 4.0,
            "high": 3.0,
            "medium": 2.0,
            "low": 1.0,
        }

        if risk_type not in self.risk_categories:
            raise ValueError(f"Unknown risk type: {risk_type}")

        sev_label = self.risk_categories[risk_type]["severity"]
        base_severity = severity_map.get(sev_label, 1.0)

        awareness_mult = self.behavioral_patterns["security_awareness"][behavior_level]["risk_multiplier"]
        compliance_mult = self.behavioral_patterns["compliance_adherence"][behavior_level]["risk_multiplier"]

        behavioral_multiplier = awareness_mult * compliance_mult

        if culture_score < 0.0:
            culture_score = 0.0
        if culture_score > 1.0:
            culture_score = 1.0

        culture_multiplier = 2.0 - culture_score

        score = base_severity * behavioral_multiplier * culture_multiplier

        if score > 10.0:
            score = 10.0

        return round(score, 2)

    def generate_alignment_matrix(self):
        """
        Generate risk-behavior-culture alignment matrix.
        """
        alignment_data = []

        behavior_levels = ["low", "medium", "high"]
        culture_scores = [0.3, 0.5, 0.7, 0.9]

        for risk_type in self.risk_categories.keys():
            for b_level in behavior_levels:
                for c_score in culture_scores:
                    risk_score = self.calculate_risk_score(risk_type, b_level, c_score)
                    status = self.get_alignment_status(risk_score)

                    alignment_data.append({
                        "risk_type": risk_type,
                        "severity": self.risk_categories[risk_type]["severity"],
                        "frequency": self.risk_categories[risk_type]["frequency"],
                        "behavior_level": b_level,
                        "culture_score": c_score,
                        "risk_score": risk_score,
                        "alignment_status": status,
                    })

        return pd.DataFrame(alignment_data)

    def get_alignment_status(self, risk_score):
        """
        Determine alignment status based on risk score.
        """
        if risk_score <= 2.0:
            return "well_aligned"
        elif risk_score <= 4.0:
            return "moderately_aligned"
        elif risk_score <= 6.0:
            return "poorly_aligned"
        else:
            return "critically_misaligned"

    def save_framework_data(self, filename="risk_framework_data.json"):
        framework_data = {
            "generated_at": datetime.now().isoformat(),
            "risk_categories": self.risk_categories,
            "behavioral_patterns": self.behavioral_patterns,
            "culture_factors": self.culture_factors,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(framework_data, f, indent=2)

        return True


def main():
    print("=== Risk-Behavior-Culture Alignment Framework ===")

    framework = RiskBehaviorCultureFramework()

    df = framework.generate_alignment_matrix()

    csv_out = "risk_alignment_matrix.csv"
    df.to_csv(csv_out, index=False)

    framework.save_framework_data("risk_framework_data.json")

    print("\n[INFO] Alignment matrix generated.")
    print(f"[INFO] Total combinations: {len(df)}")
    print("[INFO] Alignment status distribution:")
    print(df["alignment_status"].value_counts().to_string())

    print("\n[INFO] Sample data (first 10 rows):")
    print(df.head(10).to_string(index=False))

    print(f"\n[INFO] Saved: {csv_out}")
    print("[INFO] Saved: risk_framework_data.json")


if __name__ == "__main__":
    main()
