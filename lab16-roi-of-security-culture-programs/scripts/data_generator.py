import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


def generate_security_culture_data():
    """
    Generate sample security culture program metrics.

    Returns:
        DataFrame with monthly security metrics
    """
    np.random.seed(42)

    # Define time period (24 months of data)
    months = pd.date_range(end=pd.Timestamp.today().normalize(), periods=24, freq="MS")

    # Baseline metrics (start) and targets (end)
    baseline_phishing = 0.15   # 15%
    target_phishing = 0.06     # 6%

    baseline_incidents = 8     # per month
    target_incidents = 4       # per month

    baseline_compliance = 0.70  # 70%
    target_compliance = 0.95    # 95%

    # Improvement over time with diminishing returns (exponential decay towards target)
    # progress factor: 0 -> 1 over time
    t = np.arange(len(months))
    # Diminishing returns curve: 1 - exp(-k*t)
    k = 0.18
    progress = 1 - np.exp(-k * t)
    progress = progress / progress.max()  # normalize to 1 by last month

    # Generate monthly metrics with noise
    phishing_success_rate = baseline_phishing - (baseline_phishing - target_phishing) * progress
    phishing_success_rate += np.random.normal(0, 0.006, size=len(months))
    phishing_success_rate = np.clip(phishing_success_rate, 0.01, 0.30)

    security_incidents = baseline_incidents - (baseline_incidents - target_incidents) * progress
    security_incidents += np.random.normal(0, 0.7, size=len(months))
    security_incidents = np.clip(security_incidents, 0, 30)
    security_incidents = np.round(security_incidents).astype(int)

    compliance_rate = baseline_compliance + (target_compliance - baseline_compliance) * progress
    compliance_rate += np.random.normal(0, 0.01, size=len(months))
    compliance_rate = np.clip(compliance_rate, 0.40, 0.99)

    # Program costs: setup + operational
    # Setup costs heavier early; operations steady with slight growth for maturity
    setup_cost_first_month = 40000
    operational_base = 12000
    operational_growth = 0.03  # slight increase over 24 months (tools/licenses/refresh content)

    program_cost = []
    for i in range(len(months)):
        setup_component = setup_cost_first_month if i == 0 else (12000 * np.exp(-0.35 * i))
        op_component = operational_base * (1 + operational_growth * (i / (len(months) - 1)))
        # add random cost variation
        monthly_cost = setup_component + op_component + np.random.normal(0, 800)
        monthly_cost = max(5000, monthly_cost)
        program_cost.append(monthly_cost)

    program_cost = np.round(program_cost, 2)

    # Incident costs and savings
    incident_cost_per_incident = 25000

    # Baseline incident cost each month (for "no program" scenario)
    baseline_incident_cost = baseline_incidents * incident_cost_per_incident

    incident_cost = security_incidents * incident_cost_per_incident
    incident_savings = (baseline_incidents - security_incidents) * incident_cost_per_incident
    incident_savings = np.clip(incident_savings, 0, None)

    # Productivity gain (assume improved awareness reduces disruption; grows over time)
    # Use compliance improvement to influence productivity gain
    # Example: productivity gain $4k -> $12k over time
    productivity_gain = 4000 + 8000 * progress
    productivity_gain += np.random.normal(0, 500, size=len(months))
    productivity_gain = np.clip(productivity_gain, 0, None)
    productivity_gain = np.round(productivity_gain, 2)

    # Compliance savings (avoid fines, audit effort reduction)
    # Example: $2k -> $10k over time; tied to compliance rate change from baseline
    compliance_delta = compliance_rate - baseline_compliance
    compliance_savings = 2000 + (compliance_delta / (target_compliance - baseline_compliance)) * 8000
    compliance_savings += np.random.normal(0, 400, size=len(months))
    compliance_savings = np.clip(compliance_savings, 0, None)
    compliance_savings = np.round(compliance_savings, 2)

    df = pd.DataFrame({
        "month": months,
        "phishing_success_rate": np.round(phishing_success_rate, 4),
        "security_incidents": security_incidents,
        "compliance_rate": np.round(compliance_rate, 4),
        "program_cost": program_cost,
        "incident_cost": incident_cost,
        "baseline_incident_cost": baseline_incident_cost,
        "incident_savings": np.round(incident_savings, 2),
        "productivity_gain": productivity_gain,
        "compliance_savings": compliance_savings
    })

    # Total benefits column (savings + gains)
    df["total_benefits"] = np.round(
        df["incident_savings"] + df["productivity_gain"] + df["compliance_savings"],
        2
    )

    return df


def save_data_to_csv(df, filename):
    """Save DataFrame to CSV file"""
    out_path = Path(filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved generated data to: {out_path.resolve()}")


if __name__ == "__main__":
    df = generate_security_culture_data()
    save_data_to_csv(df, "../data/security_metrics.csv")
