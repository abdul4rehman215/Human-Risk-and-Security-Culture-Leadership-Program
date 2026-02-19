#!/usr/bin/env python3
"""
Cybersecurity Risk Prioritization using B.J. Fogg Model
Students: Complete the TODO sections to implement risk prioritization
"""

import json
from typing import Dict, List, Any
from fogg_model import FoggBehaviorModel


class CybersecurityRiskPrioritizer:
    """
    Risk prioritization system using Fogg behavior model
    """

    def __init__(self):
        self.fogg_model = FoggBehaviorModel()
        self.risk_database: List[Dict[str, Any]] = []
        self.prioritized_risks: List[Dict[str, Any]] = []

    def add_risk_scenario(
        self,
        risk_id: str,
        risk_name: str,
        impact_score: float,
        user_profiles: List[Dict],
        threat_frequency: float,
    ) -> None:
        """
        Add a cybersecurity risk scenario to the database
        """

        risk_scenario: Dict[str, Any] = {
            "risk_id": risk_id,
            "risk_name": risk_name,
            "impact_score": float(impact_score),
            "threat_frequency": float(threat_frequency),
            "user_profiles": user_profiles,
            "behavioral_assessments": [],
        }

        for profile in user_profiles:
            assessment = self.fogg_model.assess_cybersecurity_behavior(risk_name, profile)
            risk_scenario["behavioral_assessments"].append(assessment)

        self.risk_database.append(risk_scenario)

    def calculate_risk_priority_score(self, risk_scenario: Dict) -> float:
        """
        Formula:
        Priority = (Impact × Frequency × Behavioral_Risk_Factor) / 100
        Where Behavioral_Risk_Factor = 100 - avg_behavior_score
        """

        impact = float(risk_scenario.get("impact_score", 0))
        frequency = float(risk_scenario.get("threat_frequency", 0))

        assessments = risk_scenario.get("behavioral_assessments", [])
        if assessments:
            avg_behavior_score = (
                sum(a["scores"]["behavior_score"] for a in assessments) / len(assessments)
            )
        else:
            avg_behavior_score = 0.0

        behavioral_risk_factor = 100.0 - avg_behavior_score
        if behavioral_risk_factor < 0:
            behavioral_risk_factor = 0.0

        priority_score = (impact * frequency * behavioral_risk_factor) / 100.0

        return round(priority_score, 2)

    def prioritize_risks(self) -> List[Dict]:
        """
        Prioritize all risks in the database
        """

        self.prioritized_risks = []

        for risk in self.risk_database:
            score = self.calculate_risk_priority_score(risk)

            if score >= 70:
                level = "Critical"
            elif score >= 50:
                level = "High"
            elif score >= 30:
                level = "Medium"
            else:
                level = "Low"

            prioritized_risk = {
                "risk_id": risk.get("risk_id"),
                "risk_name": risk.get("risk_name"),
                "impact_score": risk.get("impact_score"),
                "threat_frequency": risk.get("threat_frequency"),
                "priority_score": score,
                "priority_level": level,
                "affected_users": len(risk.get("user_profiles", [])),
                "behavioral_assessments": risk.get("behavioral_assessments", []),
                "recommendations": self._generate_risk_recommendations(risk),
            }

            self.prioritized_risks.append(prioritized_risk)

        self.prioritized_risks.sort(
            key=lambda x: x.get("priority_score", 0), reverse=True
        )

        return self.prioritized_risks

    def _generate_risk_recommendations(self, risk_scenario: Dict) -> List[str]:
        """
        Generate specific recommendations
        """

        recommendations: List[str] = []

        assessments = risk_scenario.get("behavioral_assessments", [])
        impact = float(risk_scenario.get("impact_score", 0))
        frequency = float(risk_scenario.get("threat_frequency", 0))

        if assessments:
            avg_m = sum(a["scores"]["motivation"] for a in assessments) / len(assessments)
            avg_a = sum(a["scores"]["ability"] for a in assessments) / len(assessments)
            avg_t = sum(a["scores"]["trigger"] for a in assessments) / len(assessments)
        else:
            avg_m, avg_a, avg_t = 0.0, 0.0, 0.0

        if avg_m < 5:
            recommendations.append(
                "Increase motivation: run targeted awareness campaigns and leadership messaging for this risk."
            )
        if avg_a < 5:
            recommendations.append(
                "Increase ability: provide hands-on training, clear SOPs, and simplify security tools/workflows."
            )
        if avg_t < 5:
            recommendations.append(
                "Increase triggers: enable reminders, banners, simulations, and just-in-time prompts for users."
            )

        if impact >= 8:
            recommendations.append(
                "High impact detected: apply stronger controls, monitoring, and escalation procedures."
            )
        if frequency >= 8:
            recommendations.append(
                "High frequency detected: prioritize continuous controls and frequent user testing/simulations."
            )

        if not recommendations:
            recommendations.append(
                "Maintain current controls and perform periodic reassessment to ensure risk stays controlled."
            )

        return recommendations

    def generate_risk_report(self) -> str:
        """
        Generate comprehensive risk prioritization report
        """

        if not self.prioritized_risks:
            self.prioritize_risks()

        lines: List[str] = []
        lines.append("CYBERSECURITY RISK PRIORITIZATION REPORT")
        lines.append("=" * 45)
        lines.append("")

        total_risks = len(self.prioritized_risks)
        critical_count = sum(
            1 for r in self.prioritized_risks if r.get("priority_level") == "Critical"
        )
        high_count = sum(
            1 for r in self.prioritized_risks if r.get("priority_level") == "High"
        )
        medium_count = sum(
            1 for r in self.prioritized_risks if r.get("priority_level") == "Medium"
        )
        low_count = sum(
            1 for r in self.prioritized_risks if r.get("priority_level") == "Low"
        )

        lines.append("Executive Summary")
        lines.append("-" * 18)
        lines.append(f"Total Risks Assessed: {total_risks}")
        lines.append(f"Critical Risks: {critical_count}")
        lines.append(f"High Risks: {high_count}")
        lines.append(f"Medium Risks: {medium_count}")
        lines.append(f"Low Risks: {low_count}")
        lines.append("")

        for r in self.prioritized_risks:
            lines.append(f"Risk ID: {r.get('risk_id')}")
            lines.append(f"Risk Name: {r.get('risk_name')}")
            lines.append(f"Priority Level: {r.get('priority_level')}")
            lines.append(f"Priority Score: {r.get('priority_score')}")
            lines.append(f"Impact Score: {r.get('impact_score')}")
            lines.append(f"Threat Frequency: {r.get('threat_frequency')}")
            lines.append(f"Affected Users: {r.get('affected_users')}")
            lines.append("Recommendations:")
            for rec in r.get("recommendations", []):
                lines.append(f" - {rec}")
            lines.append("-" * 45)

        return "\n".join(lines)

    def export_prioritized_risks(self, filename: str) -> bool:
        """
        Export prioritized risks to JSON file
        """

        try:
            if not self.prioritized_risks:
                self.prioritize_risks()

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.prioritized_risks, f, indent=2)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    prioritizer = CybersecurityRiskPrioritizer()

    weak_users = [
        {"motivation": 3, "ability": 4, "trigger": 2},
        {"motivation": 4, "ability": 3, "trigger": 3},
    ]

    strong_users = [
        {"motivation": 8, "ability": 9, "trigger": 7},
        {"motivation": 9, "ability": 8, "trigger": 8},
    ]

    prioritizer.add_risk_scenario(
        risk_id="RISK-001",
        risk_name="Phishing Email Attacks",
        impact_score=8.5,
        user_profiles=weak_users,
        threat_frequency=9.0,
    )

    prioritizer.add_risk_scenario(
        risk_id="RISK-002",
        risk_name="Unauthorized Software Installation",
        impact_score=6.5,
        user_profiles=strong_users,
        threat_frequency=5.0,
    )

    prioritized = prioritizer.prioritize_risks()
    print("Top Priority Risks:")
    for risk in prioritized:
        print(f"- {risk['risk_name']}: {risk['priority_score']} ({risk['priority_level']})")

    report = prioritizer.generate_risk_report()
    print("\n" + report)
