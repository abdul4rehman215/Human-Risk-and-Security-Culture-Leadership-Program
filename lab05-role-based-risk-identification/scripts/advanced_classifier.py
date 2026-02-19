#!/usr/bin/env python3
"""
Advanced Role-Based Risk Classifier
Students: Implement advanced classification features
"""

import json
from datetime import datetime
from typing import Dict, Any, List


class AdvancedRiskClassifier:
    def __init__(self):
        self.risk_thresholds = {
            "CRITICAL": 80,
            "HIGH": 60,
            "MEDIUM": 40,
            "LOW": 20,
            "MINIMAL": 0,
        }

        self.department_multipliers = {
            "Executive": 1.2,
            "IT": 1.15,
            "Finance": 1.1,
            "Human Resources": 1.1,
            "Sales": 1.05,
            "Customer Service": 1.0,
        }

    def _base_score(self, role_data: Dict[str, Any]) -> float:
        access_level = float(role_data.get("access_level", 0))
        data_sensitivity = float(role_data.get("data_sensitivity", 0))
        external_exposure = float(role_data.get("external_exposure", 0))
        privilege_level = float(role_data.get("privilege_level", 0))

        score = (
            access_level * 0.3
            + data_sensitivity * 0.25
            + external_exposure * 0.25
            + privilege_level * 0.2
        ) * 10.0

        return round(score, 2)

    def _cti_modifier(self, role_type: str, cti_data: Dict[str, Any]) -> float:
        modifier = 1.0

        for cat, threats in cti_data.items():
            if not isinstance(threats, list):
                continue

            for threat in threats:
                targets = threat.get("target_roles", [])
                severity = float(threat.get("severity", 0))

                if role_type in targets:
                    modifier += severity * 0.1

        return modifier

    def calculate_advanced_risk_score(self, role_data, cti_data):
        """
        Calculate advanced risk score with department multipliers.
        """
        base = self._base_score(role_data)

        dept = role_data.get("department", "Unknown")
        dept_mult = float(self.department_multipliers.get(dept, 1.0))

        score = base * dept_mult

        role_type = role_data.get("type", "unknown")
        mod = self._cti_modifier(role_type, cti_data)

        score = score * mod

        if score > 100:
            score = 100.0

        return round(score, 2)

    def identify_risk_factors(self, role_data):
        """
        Identify specific risk factors for a role.
        """
        factors: List[str] = []

        if float(role_data.get("access_level", 0)) >= 4:
            factors.append("High system access privileges")

        if float(role_data.get("data_sensitivity", 0)) >= 4:
            factors.append("Access to sensitive data")

        if float(role_data.get("external_exposure", 0)) >= 4:
            factors.append("High external exposure")

        if float(role_data.get("privilege_level", 0)) >= 4:
            factors.append("Administrative privileges")

        role_type = role_data.get("type", "unknown")

        if role_type == "executive":
            factors.append("High-value target (executive role)")

        if role_type == "technical":
            factors.append("Elevated technical capability and privileged access")

        if role_type in ["support", "sales"]:
            factors.append("High user interaction and social engineering exposure")

        return factors

    def generate_recommendations(self, role_data, risk_level):
        """
        Generate security recommendations based on risk level.
        """
        recommendations: List[str] = []

        if risk_level in ["CRITICAL", "HIGH"]:
            recommendations.append("Enforce MFA on all accounts and privileged actions.")
            recommendations.append("Enable enhanced monitoring and alerting for this role.")
            recommendations.append("Perform frequent access reviews and least-privilege enforcement.")

        if risk_level == "MEDIUM":
            recommendations.append("Enhance email filtering and anti-phishing protections.")
            recommendations.append("Ensure endpoint protection is up-to-date and centrally monitored.")

        if float(role_data.get("external_exposure", 0)) >= 4:
            recommendations.append("Provide targeted social engineering and phishing resistance training.")

        if float(role_data.get("privilege_level", 0)) >= 4:
            recommendations.append("Implement privileged access monitoring and session recording.")

        recommendations.append("Ensure strong password policy and periodic security awareness refreshers.")

        unique = []
        for r in recommendations:
            if r not in unique:
                unique.append(r)

        return unique

    def _risk_level_from_score(self, score: float) -> str:
        if score >= self.risk_thresholds["CRITICAL"]:
            return "CRITICAL"
        if score >= self.risk_thresholds["HIGH"]:
            return "HIGH"
        if score >= self.risk_thresholds["MEDIUM"]:
            return "MEDIUM"
        if score >= self.risk_thresholds["LOW"]:
            return "LOW"
        return "MINIMAL"

    def classify_role_risk_profile(self, role_data, risk_score):
        """
        Create detailed risk profile for a role.
        """
        level = self._risk_level_from_score(risk_score)
        factors = self.identify_risk_factors(role_data)
        recs = self.generate_recommendations(role_data, level)

        profile = {
            "role_name": role_data.get("name", "Unknown"),
            "role_type": role_data.get("type", "unknown"),
            "department": role_data.get("department", "Unknown"),
            "risk_score": risk_score,
            "risk_level": level,
            "risk_factors": factors,
            "recommendations": recs,
            "generated_at": datetime.now().isoformat(),
        }

        return profile


def run_advanced_classification():
    print("Advanced Role-Based Risk Classification")
    print("=" * 45)

    try:
        with open("organizational_roles.json", "r", encoding="utf-8") as f:
            roles = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load organizational_roles.json: {e}")
        return

    try:
        with open("cti_data.json", "r", encoding="utf-8") as f:
            cti = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load cti_data.json: {e}")
        return

    classifier = AdvancedRiskClassifier()

    results: Dict[str, Any] = {}
    scores = []

    for role_id, role_data in roles.items():
        score = classifier.calculate_advanced_risk_score(role_data, cti)
        scores.append(score)

        profile = classifier.classify_role_risk_profile(role_data, score)
        results[role_id] = profile

    out_file = "advanced_risk_classification.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    dist = {}
    for _, v in results.items():
        dist[v["risk_level"]] = dist.get(v["risk_level"], 0) + 1

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
    min_score = round(min(scores), 2) if scores else 0.0
    max_score = round(max(scores), 2) if scores else 0.0

    summary_file = "classification_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("ADVANCED RISK CLASSIFICATION SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Total Roles: {len(results)}\n")
        f.write(f"Average Score: {avg_score}\n")
        f.write(f"Min Score: {min_score}\n")
        f.write(f"Max Score: {max_score}\n\n")
        f.write("Risk Level Distribution:\n")
        for lvl, count in dist.items():
            f.write(f"- {lvl}: {count}\n")

    print(f"[INFO] Advanced classification saved: {out_file}")
    print(f"[INFO] Summary report saved: {summary_file}")


if __name__ == "__main__":
    run_advanced_classification()
