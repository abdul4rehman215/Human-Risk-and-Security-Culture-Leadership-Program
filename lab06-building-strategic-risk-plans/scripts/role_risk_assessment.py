#!/usr/bin/env python3
"""
Role-Based Risk Assessment and Prioritization
I will implement role-specific risk analysis
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any


class RoleBasedRiskAssessment:
    def __init__(self):
        # Organizational roles with risk profiles
        self.organizational_roles = {
            "executive": {
                "access_level": "unrestricted",
                "target_value": "high",
                "primary_risks": ["social_engineering", "phishing", "insider_threats"],
                "risk_weight": 0.9,
            },
            "it_admin": {
                "access_level": "administrative",
                "target_value": "critical",
                "primary_risks": ["insider_threats", "weak_passwords", "unsecured_devices"],
                "risk_weight": 0.95,
            },
            "finance": {
                "access_level": "sensitive",
                "target_value": "high",
                "primary_risks": ["phishing", "social_engineering", "weak_passwords"],
                "risk_weight": 0.85,
            },
            "general_staff": {
                "access_level": "basic",
                "target_value": "low",
                "primary_risks": ["phishing", "weak_passwords", "unsecured_devices"],
                "risk_weight": 0.5,
            },
        }

        # Risk impact across different dimensions
        self.risk_impact_matrix = {
            "phishing": {"financial": 8, "operational": 7, "reputational": 9, "legal": 6},
            "weak_passwords": {"financial": 6, "operational": 8, "reputational": 5, "legal": 4},
            "social_engineering": {"financial": 9, "operational": 8, "reputational": 9, "legal": 7},
            "insider_threats": {"financial": 10, "operational": 9, "reputational": 8, "legal": 9},
            "unsecured_devices": {"financial": 5, "operational": 6, "reputational": 4, "legal": 3},
        }

    def calculate_role_risk_score(self, role, risk_type):
        """
        Calculate risk score for specific role and risk type.

        Args:
            role: Role name from organizational_roles
            risk_type: Risk type from risk_impact_matrix

        Returns:
            Float risk score (0-10 scale)
        """
        impacts = self.risk_impact_matrix[risk_type]
        mean_impact = float(np.mean(list(impacts.values())))  # 0-10-ish

        weight = float(self.organizational_roles[role]["risk_weight"])
        score = mean_impact * weight

        # Check if primary risk (multiply by 1.3 if yes)
        if risk_type in self.organizational_roles[role]["primary_risks"]:
            score *= 1.3

        # Cap at 10.0
        if score > 10.0:
            score = 10.0

        return round(score, 2)

    def get_priority_level(self, risk_score):
        """
        Determine priority level based on risk score.

        Returns: 'critical', 'high', 'medium', or 'low'
        """
        if risk_score >= 8.0:
            return "critical"
        elif risk_score >= 6.0:
            return "high"
        elif risk_score >= 4.0:
            return "medium"
        else:
            return "low"

    def generate_role_risk_matrix(self):
        """
        Generate comprehensive role-risk assessment matrix.

        Returns:
            DataFrame with role-risk combinations
        """
        assessment_data = []

        for role in self.organizational_roles.keys():
            for risk_type in self.risk_impact_matrix.keys():
                score = self.calculate_role_risk_score(role, risk_type)
                priority = self.get_priority_level(score)

                assessment_data.append({
                    "role": role,
                    "access_level": self.organizational_roles[role]["access_level"],
                    "target_value": self.organizational_roles[role]["target_value"],
                    "risk_type": risk_type,
                    "risk_score": score,
                    "priority_level": priority,
                    "is_primary_risk": risk_type in self.organizational_roles[role]["primary_risks"],
                })

        return pd.DataFrame(assessment_data)

    def get_timeline_recommendation(self, priority):
        """Get recommended timeline based on priority level."""
        timelines = {
            "critical": "immediate (1-2 weeks)",
            "high": "urgent (1 month)",
            "medium": "planned (3 months)",
            "low": "routine (6 months)",
        }
        return timelines.get(priority, "planned (3 months)")

    def create_prioritized_action_plan(self, assessment_df):
        """
        Create prioritized action plan based on assessment.

        Returns:
            List of action items sorted by priority
        """
        action_plan: List[Dict[str, Any]] = []

        priority_order = ["critical", "high", "medium", "low"]

        for p in priority_order:
            subset = assessment_df[assessment_df["priority_level"] == p]
            if subset.empty:
                continue

            # top 3 affected roles (by average score within this priority)
            role_avg = subset.groupby("role")["risk_score"].mean().sort_values(ascending=False)
            top_roles = list(role_avg.head(3).index)

            # top 3 risks in this priority
            risk_avg = subset.groupby("risk_type")["risk_score"].mean().sort_values(ascending=False)
            top_risks = list(risk_avg.head(3).index)

            avg_score = round(float(subset["risk_score"].mean()), 2)

            # Suggest mitigation strategies (simple templates)
            mitigations = []
            if "phishing" in top_risks or "social_engineering" in top_risks:
                mitigations.append("Run phishing simulations and targeted awareness training.")
                mitigations.append("Strengthen email security controls (DMARC/SPF/DKIM, filtering).")
            if "weak_passwords" in top_risks:
                mitigations.append("Enforce MFA and strong password policies; deploy password manager.")
            if "insider_threats" in top_risks:
                mitigations.append("Implement privileged access management and logging/monitoring.")
                mitigations.append("Perform regular access reviews and segregation of duties.")
            if "unsecured_devices" in top_risks:
                mitigations.append("Ensure endpoint patching, EDR coverage, and device encryption.")

            action_plan.append({
                "priority_level": p,
                "average_risk_score": avg_score,
                "top_roles": top_roles,
                "top_risks": top_risks,
                "timeline": self.get_timeline_recommendation(p),
                "mitigation_strategies": list(dict.fromkeys(mitigations)),  # unique preserving order
                "instances": int(len(subset)),
            })

        # Sort by average risk score (descending)
        action_plan.sort(key=lambda x: x["average_risk_score"], reverse=True)
        return action_plan

    def save_assessment_results(self, assessment_df, action_plan):
        """Save assessment results to files."""
        # Save assessment_df to CSV
        assessment_df.to_csv("role_based_risk_assessment.csv", index=False)

        # Save action_plan to JSON
        with open("prioritized_action_plan.json", "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "action_plan": action_plan
            }, f, indent=2)

        # Save organizational_roles to JSON
        with open("organizational_roles.json", "w", encoding="utf-8") as f:
            json.dump(self.organizational_roles, f, indent=2)

        return True


def main():
    print("=== Role-Based Risk Assessment ===")

    assessment = RoleBasedRiskAssessment()

    df = assessment.generate_role_risk_matrix()
    action_plan = assessment.create_prioritized_action_plan(df)

    assessment.save_assessment_results(df, action_plan)

    print("\n[INFO] Role-risk assessment created.")
    print(f"[INFO] Total role-risk combinations: {len(df)}")
    print("[INFO] Priority distribution:")
    print(df["priority_level"].value_counts().to_string())

    print("\n[INFO] Top 3 priority actions:")
    for item in action_plan[:3]:
        print(f"- Priority: {item['priority_level']} | Avg Score: {item['average_risk_score']} | Timeline: {item['timeline']}")
        print(f"  Top Roles: {', '.join(item['top_roles'])}")
        print(f"  Top Risks: {', '.join(item['top_risks'])}")

    print("\n[INFO] Saved outputs:")
    print(" - role_based_risk_assessment.csv")
    print(" - prioritized_action_plan.json")
    print(" - organizational_roles.json")


if __name__ == "__main__":
    main()
