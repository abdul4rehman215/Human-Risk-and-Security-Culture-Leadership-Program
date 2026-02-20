#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
from datetime import datetime
from pathlib import Path


class BehaviorAnalyzer:
    def __init__(self, data_file):
        """Initialize analyzer with behavior data."""
        self.df = pd.read_csv(data_file)
        self.df["Training_Date"] = pd.to_datetime(self.df["Training_Date"])

        # Derived fields
        self.df["Knowledge_Improvement"] = self.df["Post_Score"] - self.df["Pre_Score"]
        self.df["Phishing_Passes"] = (
            (self.df["Phishing_Test_1"] == "Passed").astype(int) +
            (self.df["Phishing_Test_2"] == "Passed").astype(int) +
            (self.df["Phishing_Test_3"] == "Passed").astype(int)
        )

    def calculate_summary_statistics(self):
        """
        Calculate key summary statistics.
        """
        total = len(self.df)

        pre_avg = float(self.df["Pre_Score"].mean())
        post_avg = float(self.df["Post_Score"].mean())
        improvement_avg = float(self.df["Knowledge_Improvement"].mean())
        improvement_median = float(self.df["Knowledge_Improvement"].median())
        improvement_std = float(self.df["Knowledge_Improvement"].std(ddof=1))

        behavior_avg = float(self.df["Behavior_Score"].mean())

        # Compliance and security controls
        pwd_rate = float((self.df["Password_Compliance"] == "Yes").mean()) * 100.0
        mfa_rate = float((self.df["MFA_Enabled"] == "Yes").mean()) * 100.0

        # Phishing pass rates per simulation
        sim1_rate = float((self.df["Phishing_Test_1"] == "Passed").mean()) * 100.0
        sim2_rate = float((self.df["Phishing_Test_2"] == "Passed").mean()) * 100.0
        sim3_rate = float((self.df["Phishing_Test_3"] == "Passed").mean()) * 100.0

        return {
            "total_employees": int(total),
            "pre_avg": round(pre_avg, 2),
            "post_avg": round(post_avg, 2),
            "improvement_avg": round(improvement_avg, 2),
            "improvement_median": round(improvement_median, 2),
            "improvement_std": round(improvement_std, 2) if not np.isnan(improvement_std) else 0.0,
            "behavior_avg": round(behavior_avg, 2),
            "password_compliance_rate_pct": round(pwd_rate, 2),
            "mfa_enabled_rate_pct": round(mfa_rate, 2),
            "phishing_pass_rate_pct": {
                "sim1": round(sim1_rate, 2),
                "sim2": round(sim2_rate, 2),
                "sim3": round(sim3_rate, 2),
            },
        }

    def analyze_by_department(self):
        """
        Analyze behavior metrics grouped by department.
        """
        grp = self.df.groupby("Department", as_index=False).agg(
            employees=("Employee_ID", "count"),
            pre_avg=("Pre_Score", "mean"),
            post_avg=("Post_Score", "mean"),
            improvement_avg=("Knowledge_Improvement", "mean"),
            behavior_avg=("Behavior_Score", "mean"),
            pwd_compliance=("Password_Compliance", lambda s: float((s == "Yes").mean()) * 100.0),
            mfa_enabled=("MFA_Enabled", lambda s: float((s == "Yes").mean()) * 100.0),
            phishing_sim1=("Phishing_Test_1", lambda s: float((s == "Passed").mean()) * 100.0),
            phishing_sim2=("Phishing_Test_2", lambda s: float((s == "Passed").mean()) * 100.0),
            phishing_sim3=("Phishing_Test_3", lambda s: float((s == "Passed").mean()) * 100.0),
        )

        # Identify best/worst by behavior_avg
        best = grp.sort_values("behavior_avg", ascending=False).head(1)[["Department", "behavior_avg"]]
        worst = grp.sort_values("behavior_avg", ascending=True).head(1)[["Department", "behavior_avg"]]

        best_dep = best.iloc[0]["Department"]
        worst_dep = worst.iloc[0]["Department"]

        return grp, {"best_department": best_dep, "worst_department": worst_dep}

    def analyze_phishing_performance(self):
        """
        Analyze phishing simulation results over time.
        """
        sim_rates = {
            "sim1_pass_rate_pct": float((self.df["Phishing_Test_1"] == "Passed").mean()) * 100.0,
            "sim2_pass_rate_pct": float((self.df["Phishing_Test_2"] == "Passed").mean()) * 100.0,
            "sim3_pass_rate_pct": float((self.df["Phishing_Test_3"] == "Passed").mean()) * 100.0,
        }

        improvement = sim_rates["sim3_pass_rate_pct"] - sim_rates["sim1_pass_rate_pct"]

        by_dept = self.df.groupby("Department").apply(
            lambda g: pd.Series({
                "sim1": float((g["Phishing_Test_1"] == "Passed").mean()) * 100.0,
                "sim2": float((g["Phishing_Test_2"] == "Passed").mean()) * 100.0,
                "sim3": float((g["Phishing_Test_3"] == "Passed").mean()) * 100.0,
            })
        ).reset_index()

        # Employees needing additional training: failed sim3 OR passed 0/3 overall
        needs_training = self.df[
            (self.df["Phishing_Test_3"] == "Failed") | (self.df["Phishing_Passes"] == 0)
        ][["Employee_ID", "Department", "Phishing_Test_1", "Phishing_Test_2", "Phishing_Test_3", "Behavior_Score"]]

        return {
            "overall_pass_rates_pct": {k: round(v, 2) for k, v in sim_rates.items()},
            "overall_improvement_sim1_to_sim3_pct_points": round(float(improvement), 2),
            "by_department_pass_rates_pct": by_dept.round(2).to_dict(orient="records"),
            "employees_needing_additional_training": needs_training.to_dict(orient="records"),
        }

    def assess_risk_levels(self):
        """
        Analyze risk distribution and identify high-risk employees.
        """
        counts = self.df["Risk_Level"].value_counts().to_dict()
        total = len(self.df)

        pct = {k: round((v / total) * 100.0, 2) for k, v in counts.items()}

        high_risk = self.df[self.df["Risk_Level"] == "High"][
            ["Employee_ID", "Department", "Behavior_Score", "Knowledge_Improvement", "Incident_Reports", "Password_Compliance", "MFA_Enabled"]
        ].sort_values(["Behavior_Score", "Incident_Reports"], ascending=[True, False])

        # Risk factor patterns by department
        risk_by_dept = self.df.groupby(["Department", "Risk_Level"]).size().reset_index(name="count")

        return {
            "risk_level_counts": {k: int(v) for k, v in counts.items()},
            "risk_level_percentages": pct,
            "high_risk_employees": high_risk.to_dict(orient="records"),
            "risk_by_department": risk_by_dept.to_dict(orient="records"),
        }

    def generate_recommendations(self):
        """
        Generate actionable recommendations based on analysis.
        """
        recs = []

        summary = self.calculate_summary_statistics()
        dept_df, bestworst = self.analyze_by_department()
        phishing = self.analyze_phishing_performance()
        risk = self.assess_risk_levels()

        # Knowledge improvement
        if summary["improvement_avg"] < 20:
            recs.append("Increase training reinforcement: add short weekly micro-lessons to improve knowledge retention.")
        else:
            recs.append("Maintain current training structure; knowledge improvement is trending positively.")

        # Phishing performance
        sim3 = phishing["overall_pass_rates_pct"]["sim3_pass_rate_pct"]
        if sim3 < 80:
            recs.append("Run targeted anti-phishing simulations and coaching for employees who failed the latest simulation.")
        else:
            recs.append("Phishing resilience is strong; continue quarterly simulations to sustain performance.")

        # Compliance
        if summary["password_compliance_rate_pct"] < 85:
            recs.append("Improve password compliance with policy reminders + password manager rollout and spot checks.")
        if summary["mfa_enabled_rate_pct"] < 90:
            recs.append("Increase MFA adoption: enforce MFA for high-privilege roles and run MFA enablement campaigns.")

        # High risk employees
        high_count = risk["risk_level_counts"].get("High", 0)
        if high_count > 0:
            recs.append(f"Prioritize interventions for {high_count} high-risk employees: 1:1 coaching and follow-up assessments.")

        # Department attention
        worst = bestworst["worst_department"]
        recs.append(f"Department needing most attention: {worst}. Provide tailored sessions and manager accountability metrics.")

        # Incident reporting
        avg_reports = float(self.df["Incident_Reports"].mean())
        if avg_reports < 0.5:
            recs.append("Encourage incident reporting: simplify the reporting process and communicate 'reporting is rewarded'.")
        else:
            recs.append("Incident reporting activity is present; ensure triage processes and feedback loops are timely.")

        return recs

    def export_results(self, output_file):
        """
        Export analysis results to JSON for visualization.
        """
        summary = self.calculate_summary_statistics()
        dept_df, bestworst = self.analyze_by_department()
        phishing = self.analyze_phishing_performance()
        risk = self.assess_risk_levels()
        recs = self.generate_recommendations()

        out = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
            "departments": dept_df.round(2).to_dict(orient="records"),
            "best_worst": bestworst,
            "phishing": phishing,
            "risk": risk,
            "recommendations": recs,
        }

        with open(output_file, "w") as f:
            json.dump(out, f, indent=2)

        print(f"Exported analysis results to: {output_file}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "behavior_data.csv"
    out_json = project_root / "data" / "analysis_results.json"

    analyzer = BehaviorAnalyzer(data_file)

    summary = analyzer.calculate_summary_statistics()
    dept_df, bestworst = analyzer.analyze_by_department()
    phishing = analyzer.analyze_phishing_performance()
    risk = analyzer.assess_risk_levels()
    recs = analyzer.generate_recommendations()

    print("\n=== BEHAVIOR ANALYSIS REPORT ===")
    print(f"Employees analyzed: {summary['total_employees']}")
    print(f"Avg Pre Score: {summary['pre_avg']} | Avg Post Score: {summary['post_avg']}")
    print(f"Avg Improvement: {summary['improvement_avg']} (median {summary['improvement_median']})")
    print(f"Avg Behavior Score: {summary['behavior_avg']}")
    print(f"Password Compliance: {summary['password_compliance_rate_pct']}%")
    print(f"MFA Enabled: {summary['mfa_enabled_rate_pct']}%")
    print("Phishing Pass Rates (%):", summary["phishing_pass_rate_pct"])
    print(f"Best Department: {bestworst['best_department']} | Worst Department: {bestworst['worst_department']}")

    print("\nTop Department Summary (first 10 rows):")
    print(dept_df.round(2).head(10).to_string(index=False))

    print("\nRisk Distribution:", risk["risk_level_percentages"])
    print(f"Employees needing additional phishing training: {len(phishing['employees_needing_additional_training'])}")

    print("\n=== RECOMMENDATIONS ===")
    for i, r in enumerate(recs, start=1):
        print(f"{i}. {r}")

    analyzer.export_results(out_json)
    print(f"\nReport generated at (UTC): {datetime.utcnow().isoformat()}Z\n")


if __name__ == "__main__":
    main()
