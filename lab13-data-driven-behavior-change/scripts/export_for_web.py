#!/usr/bin/env python3
import pandas as pd
import json
from datetime import datetime


def export_dashboard_data(input_file, output_file):
    """
    Export behavior data in format suitable for web dashboard.
    """
    df = pd.read_csv(input_file)
    df["Training_Date"] = pd.to_datetime(df["Training_Date"])
    df["Knowledge_Improvement"] = df["Post_Score"] - df["Pre_Score"]

    # Summary statistics
    summary = {
        "total_employees": int(len(df)),
        "pre_avg": round(float(df["Pre_Score"].mean()), 2),
        "post_avg": round(float(df["Post_Score"].mean()), 2),
        "improvement_avg": round(float(df["Knowledge_Improvement"].mean()), 2),
        "behavior_avg": round(float(df["Behavior_Score"].mean()), 2),
        "password_compliance_rate_pct": round(float((df["Password_Compliance"] == "Yes").mean()) * 100.0, 2),
        "mfa_enabled_rate_pct": round(float((df["MFA_Enabled"] == "Yes").mean()) * 100.0, 2),
        "phishing_pass_rate_pct": {
            "sim1": round(float((df["Phishing_Test_1"] == "Passed").mean()) * 100.0, 2),
            "sim2": round(float((df["Phishing_Test_2"] == "Passed").mean()) * 100.0, 2),
            "sim3": round(float((df["Phishing_Test_3"] == "Passed").mean()) * 100.0, 2),
        },
    }

    # Aggregate by department
    dept = df.groupby("Department", as_index=False).agg(
        employees=("Employee_ID", "count"),
        pre_avg=("Pre_Score", "mean"),
        post_avg=("Post_Score", "mean"),
        improvement_avg=("Knowledge_Improvement", "mean"),
        behavior_avg=("Behavior_Score", "mean"),
    )
    dept = dept.round(2)

    # Risk distribution
    risk_counts = df["Risk_Level"].value_counts().to_dict()
    risk_pct = {k: round((v / len(df)) * 100.0, 2) for k, v in risk_counts.items()}

    # Phishing overall pass rates
    phishing = {
        "overall_pass_rates_pct": {
            "sim1_pass_rate_pct": round(float((df["Phishing_Test_1"] == "Passed").mean()) * 100.0, 2),
            "sim2_pass_rate_pct": round(float((df["Phishing_Test_2"] == "Passed").mean()) * 100.0, 2),
            "sim3_pass_rate_pct": round(float((df["Phishing_Test_3"] == "Passed").mean()) * 100.0, 2),
        }
    }

    out = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summary": summary,
        "departments": dept.to_dict(orient="records"),
        "risk": {
            "risk_level_counts": {k: int(v) for k, v in risk_counts.items()},
            "risk_level_percentages": risk_pct,
        },
        "phishing": phishing,
    }

    with open(output_file, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Exported dashboard data to: {output_file}")


if __name__ == "__main__":
    export_dashboard_data(
        "../data/behavior_data.csv",
        "../web/dashboard_data.json"
    )
