#!/usr/bin/env python3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path


def calculate_behavior_score(metrics):
    """
    Calculate overall behavior score from individual metrics.
    Returns: Float score between 0-10
    """
    # Knowledge improvement (20%)
    pre = metrics["Pre_Score"]
    post = metrics["Post_Score"]
    improvement = max(0, post - pre)  # 0..100
    improvement_norm = min(1.0, improvement / 50.0)  # cap at 50-point improvement

    # Phishing performance (30%)
    phishing_passes = metrics["Phishing_Passes"]  # 0..3
    phishing_norm = phishing_passes / 3.0

    # Policy compliance (25%)
    pwd_norm = 1.0 if metrics["Password_Compliance"] == "Yes" else 0.0

    # Incident reporting (15%)
    reports = metrics["Incident_Reports"]
    if reports == 0:
        incident_norm = 0.4
    elif reports <= 2:
        incident_norm = 1.0
    elif reports <= 4:
        incident_norm = 0.7
    else:
        incident_norm = 0.4

    # Tool usage (10%)
    mfa_norm = 1.0 if metrics["MFA_Enabled"] == "Yes" else 0.0

    score_0_1 = (
        0.20 * improvement_norm +
        0.30 * phishing_norm +
        0.25 * pwd_norm +
        0.15 * incident_norm +
        0.10 * mfa_norm
    )

    return round(score_0_1 * 10.0, 2)


def assign_risk_level(behavior_score):
    """
    Assign risk levels (Low/Medium/High) based on behavior score.
    """
    if behavior_score >= 7.5:
        return "Low"
    if behavior_score >= 5.0:
        return "Medium"
    return "High"


def generate_behavior_data(num_employees=50):
    """
    Generate sample behavior change data for analysis.
    """
    departments = ["IT", "Finance", "HR", "Marketing", "Operations", "Legal", "Executive"]

    dept_weights = {
        "IT": 0.16,
        "Finance": 0.14,
        "HR": 0.14,
        "Marketing": 0.12,
        "Operations": 0.20,
        "Legal": 0.10,
        "Executive": 0.14,
    }

    dept_choices = list(dept_weights.keys())
    dept_probs = np.array(list(dept_weights.values()))
    dept_probs = dept_probs / dept_probs.sum()

    start_date = datetime.now() - timedelta(days=90)

    records = []
    for i in range(1, num_employees + 1):
        emp_id = f"EMP{i:03d}"
        dept = np.random.choice(dept_choices, p=dept_probs)

        training_date = start_date + timedelta(days=random.randint(0, 90))
        training_date_str = training_date.strftime("%Y-%m-%d")

        dept_pre_base = {
            "IT": 40,
            "Finance": 38,
            "HR": 35,
            "Marketing": 33,
            "Operations": 30,
            "Legal": 40,
            "Executive": 42,
        }.get(dept, 35)

        pre = int(np.clip(np.random.normal(loc=dept_pre_base, scale=12), 0, 100))

        improvement = int(np.clip(np.random.normal(loc=35, scale=12), 5, 65))
        post = int(np.clip(pre + improvement, 0, 100))

        def sim_result(pass_prob):
            return "Passed" if random.random() < pass_prob else "Failed"

        p1 = min(0.90, max(0.10, (pre / 120.0)))
        p2 = min(0.95, max(0.15, (post / 120.0)))
        p3 = min(0.98, max(0.20, (post / 115.0)))

        phishing_1 = sim_result(p1)
        phishing_2 = sim_result(p2)
        phishing_3 = sim_result(p3)

        phishing_passes = [phishing_1, phishing_2, phishing_3].count("Passed")

        pwd_prob = min(0.95, max(0.20, post / 110.0))
        password_compliance = "Yes" if random.random() < pwd_prob else "No"

        mfa_prob = 0.65
        if dept in ("IT", "Legal", "Executive"):
            mfa_prob += 0.10
        if password_compliance == "Yes":
            mfa_prob += 0.10
        mfa_enabled = "Yes" if random.random() < min(0.95, mfa_prob) else "No"

        if post < 60:
            base_reports = random.randint(1, 5)
        elif post < 75:
            base_reports = random.randint(0, 3)
        else:
            base_reports = random.randint(0, 2)

        if dept == "Operations":
            base_reports = min(6, base_reports + random.randint(0, 2))

        metrics = {
            "Pre_Score": pre,
            "Post_Score": post,
            "Phishing_Passes": phishing_passes,
            "Password_Compliance": password_compliance,
            "MFA_Enabled": mfa_enabled,
            "Incident_Reports": base_reports,
        }

        behavior_score = calculate_behavior_score(metrics)
        risk_level = assign_risk_level(behavior_score)

        record = {
            "Employee_ID": emp_id,
            "Department": dept,
            "Training_Date": training_date_str,
            "Pre_Score": pre,
            "Post_Score": post,
            "Phishing_Test_1": phishing_1,
            "Phishing_Test_2": phishing_2,
            "Phishing_Test_3": phishing_3,
            "Password_Compliance": password_compliance,
            "MFA_Enabled": mfa_enabled,
            "Incident_Reports": base_reports,
            "Behavior_Score": behavior_score,
            "Risk_Level": risk_level,
        }

        records.append(record)

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    out_csv = project_root / "data" / "behavior_data.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    df = generate_behavior_data(50)
    df.to_csv(out_csv, index=False)

    print(f"Generated {len(df)} employee records")
    print(f"Saved to: {out_csv}")
