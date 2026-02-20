#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
from datetime import datetime
from pathlib import Path


class PatternDetector:
    def __init__(self, data_file):
        """Initialize pattern detector with behavior data."""
        self.df = pd.read_csv(data_file)
        self.df["Training_Date"] = pd.to_datetime(self.df["Training_Date"])
        self.df["Knowledge_Improvement"] = self.df["Post_Score"] - self.df["Pre_Score"]
        self.df["Phishing_Passes"] = (
            (self.df["Phishing_Test_1"] == "Passed").astype(int) +
            (self.df["Phishing_Test_2"] == "Passed").astype(int) +
            (self.df["Phishing_Test_3"] == "Passed").astype(int)
        )

    def identify_improvement_trends(self):
        """
        Identify employees showing improvement.
        """
        # Consistent improvers: improvement >= 25 and passed at least 2 phishing sims and behavior score >= 7
        improvers = self.df[
            (self.df["Knowledge_Improvement"] >= 25) &
            (self.df["Phishing_Passes"] >= 2) &
            (self.df["Behavior_Score"] >= 7.0)
        ][["Employee_ID", "Department", "Knowledge_Improvement", "Phishing_Passes", "Behavior_Score"]]

        # Employees needing attention: improvement < 15 OR failed sim3 OR behavior score < 5
        needs_attention = self.df[
            (self.df["Knowledge_Improvement"] < 15) |
            (self.df["Phishing_Test_3"] == "Failed") |
            (self.df["Behavior_Score"] < 5.0)
        ][["Employee_ID", "Department", "Knowledge_Improvement", "Phishing_Test_3", "Behavior_Score", "Risk_Level"]]

        return {
            "consistent_improvers": improvers.to_dict(orient="records"),
            "employees_needing_attention": needs_attention.to_dict(orient="records"),
        }

    def detect_risk_factors(self):
        """
        Identify common factors among high-risk employees.
        """
        high = self.df[self.df["Risk_Level"] == "High"].copy()
        if high.empty:
            return {"note": "No high-risk employees found in dataset."}

        # Factor rates in high risk group
        pwd_no_rate = float((high["Password_Compliance"] == "No").mean()) * 100.0
        mfa_no_rate = float((high["MFA_Enabled"] == "No").mean()) * 100.0
        avg_reports = float(high["Incident_Reports"].mean())
        avg_phishing_passes = float(high["Phishing_Passes"].mean())
        avg_improvement = float(high["Knowledge_Improvement"].mean())

        # Department concentration
        dept_counts = high["Department"].value_counts().to_dict()

        # Correlations (numeric proxies)
        dfc = self.df.copy()
        dfc["Password_Compliance_Num"] = (dfc["Password_Compliance"] == "Yes").astype(int)
        dfc["MFA_Enabled_Num"] = (dfc["MFA_Enabled"] == "Yes").astype(int)
        dfc["Risk_Num"] = dfc["Risk_Level"].map({"Low": 1, "Medium": 2, "High": 3}).fillna(2)

        corr = {}
        for col in [
            "Behavior_Score",
            "Knowledge_Improvement",
            "Phishing_Passes",
            "Password_Compliance_Num",
            "MFA_Enabled_Num",
            "Incident_Reports",
        ]:
            corr[col] = float(dfc[col].corr(dfc["Risk_Num"]))

        return {
            "high_risk_count": int(len(high)),
            "high_risk_department_counts": {k: int(v) for k, v in dept_counts.items()},
            "high_risk_pwd_noncompliance_rate_pct": round(pwd_no_rate, 2),
            "high_risk_mfa_disabled_rate_pct": round(mfa_no_rate, 2),
            "high_risk_avg_incident_reports": round(avg_reports, 2),
            "high_risk_avg_phishing_passes": round(avg_phishing_passes, 2),
            "high_risk_avg_knowledge_improvement": round(avg_improvement, 2),
            "correlation_with_risk_numeric_proxy": {
                k: round(v, 3) if not np.isnan(v) else 0.0 for k, v in corr.items()
            },
        }

    def predict_future_performance(self):
        """
        Predict future behavior scores based on simple trend projection.
        """
        # Very simple heuristic prediction:
        # future_score = current + (improvement_norm * 1.0) + (phishing_passes * 0.2) - (incident_reports * 0.1)
        dfp = self.df.copy()
        dfp["improvement_norm"] = (dfp["Knowledge_Improvement"].clip(lower=0) / 50.0).clip(upper=1.0)

        dfp["predicted_behavior_score_30d"] = (
            dfp["Behavior_Score"] +
            (dfp["improvement_norm"] * 1.0) +
            (dfp["Phishing_Passes"] * 0.2) -
            (dfp["Incident_Reports"] * 0.1)
        ).clip(lower=0, upper=10).round(2)

        # Identify at-risk employees: predicted score < 5.0
        at_risk = dfp[dfp["predicted_behavior_score_30d"] < 5.0][
            ["Employee_ID", "Department", "Behavior_Score", "predicted_behavior_score_30d", "Risk_Level"]
        ].sort_values("predicted_behavior_score_30d", ascending=True)

        return {
            "predictions": dfp[["Employee_ID", "Department", "predicted_behavior_score_30d"]].to_dict(orient="records"),
            "at_risk_employees": at_risk.to_dict(orient="records"),
        }

    def generate_intervention_recommendations(self):
        """
        Generate targeted intervention recommendations.
        """
        recs = {}

        for _, row in self.df.iterrows():
            emp = row["Employee_ID"]
            dept = row["Department"]
            risk = row["Risk_Level"]
            score = float(row["Behavior_Score"])
            sim3 = row["Phishing_Test_3"]
            pwd = row["Password_Compliance"]
            mfa = row["MFA_Enabled"]
            reports = int(row["Incident_Reports"])
            improvement = int(row["Knowledge_Improvement"])

            actions = []

            if risk == "High" or score < 5.0:
                actions.append("Assign 1:1 security coaching session within 7 days.")
                actions.append("Schedule mandatory refresher training and re-test within 14 days.")

            if sim3 == "Failed":
                actions.append("Enroll in phishing simulation remediation module + follow-up simulation.")

            if pwd == "No":
                actions.append("Require password manager onboarding + password policy compliance check.")

            if mfa == "No":
                actions.append("Enable MFA assistance session; enforce MFA on critical services.")

            if reports >= 4:
                actions.append("Review incident patterns with manager; improve workflow and reduce risky behaviors.")
            elif reports == 0 and risk != "Low":
                actions.append("Promote reporting culture: remind how/when to report suspicious activity.")

            if improvement < 15:
                actions.append("Add weekly microlearning nudges for 4 weeks to boost knowledge retention.")

            if not actions:
                actions.append("Maintain current cadence; send quarterly refresher and monthly security tip.")

            recs[emp] = {
                "employee_id": emp,
                "department": dept,
                "risk_level": risk,
                "behavior_score": score,
                "recommended_actions": actions,
            }

        return recs


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "behavior_data.csv"
    out_file = project_root / "data" / "pattern_insights.json"

    detector = PatternDetector(data_file)

    trends = detector.identify_improvement_trends()
    risk_factors = detector.detect_risk_factors()
    predictions = detector.predict_future_performance()
    interventions = detector.generate_intervention_recommendations()

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "trends": trends,
        "risk_factors": risk_factors,
        "predictions": predictions,
        "interventions": interventions,
    }

    with open(out_file, "w") as f:
        json.dump(report, f, indent=2)

    print("=== PATTERN DETECTION REPORT COMPLETE ===")
    print(f"Saved: {out_file}")
    print(f"Consistent improvers: {len(trends['consistent_improvers'])}")
    print(f"Employees needing attention: {len(trends['employees_needing_attention'])}")
    if isinstance(risk_factors, dict) and "high_risk_count" in risk_factors:
        print(f"High-risk employees: {risk_factors['high_risk_count']}")
    print(f"At-risk predicted (next 30d): {len(predictions['at_risk_employees'])}")
    print(f"Interventions generated: {len(interventions)}")


if __name__ == "__main__":
    main()
