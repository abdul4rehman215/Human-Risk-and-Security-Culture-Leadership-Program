#!/usr/bin/env python3
"""
Organizational Security Behavior Assessment Tool
Uses:
- FoggBehaviorModel (behavior scoring)
- CybersecurityRiskPrioritizer (risk priority scoring)

Outputs:
- A formatted text report to stdout
- A JSON report file: org_risk_report.json
"""

import json
import datetime
from typing import Dict, List, Any

from fogg_model import FoggBehaviorModel
from risk_prioritization import CybersecurityRiskPrioritizer


def build_department_profiles() -> Dict[str, List[Dict[str, float]]]:
    """
    Defines multiple departments with different security profiles.
    """

    departments = {
        "HR": [
            {"motivation": 7, "ability": 4, "trigger": 5},
            {"motivation": 6, "ability": 4, "trigger": 4},
        ],
        "Marketing": [
            {"motivation": 6, "ability": 4, "trigger": 4},
            {"motivation": 5, "ability": 5, "trigger": 4},
        ],
        "Finance": [
            {"motivation": 7, "ability": 5, "trigger": 5},
            {"motivation": 6, "ability": 5, "trigger": 4},
        ],
        "IT": [
            {"motivation": 5, "ability": 9, "trigger": 4},
            {"motivation": 6, "ability": 8, "trigger": 5},
        ],
        "Executives": [
            {"motivation": 6, "ability": 3, "trigger": 3},
            {"motivation": 5, "ability": 3, "trigger": 2},
        ],
    }

    return departments


def build_common_risks() -> List[Dict[str, Any]]:
    """
    Defines common cybersecurity risks across the organization.
    """

    return [
        {"risk_id": "ORG-RISK-001", "risk_name": "Phishing / Credential Harvesting", "impact_score": 9.5, "threat_frequency": 9.0},
        {"risk_id": "ORG-RISK-002", "risk_name": "Business Email Compromise (BEC)", "impact_score": 9.8, "threat_frequency": 8.5},
        {"risk_id": "ORG-RISK-003", "risk_name": "Weak Password Hygiene", "impact_score": 8.0, "threat_frequency": 7.5},
        {"risk_id": "ORG-RISK-004", "risk_name": "Unauthorized Software Installation", "impact_score": 6.5, "threat_frequency": 5.5},
        {"risk_id": "ORG-RISK-005", "risk_name": "Data Mishandling / Sharing Errors", "impact_score": 8.5, "threat_frequency": 6.5},
        {"risk_id": "ORG-RISK-006", "risk_name": "Privilege Misuse / Misconfiguration", "impact_score": 8.8, "threat_frequency": 6.0},
    ]


def assess_department_behaviors(
    fogg: FoggBehaviorModel,
    departments: Dict[str, List[Dict[str, float]]]
) -> Dict[str, Any]:

    behaviors = [
        "Password Management",
        "Phishing Awareness",
        "Software Installation Compliance",
        "Incident Reporting",
    ]

    dept_results: Dict[str, Any] = {}

    for dept, profiles in departments.items():
        assessments = []

        for behavior in behaviors:
            for profile in profiles:
                assessments.append(
                    fogg.assess_cybersecurity_behavior(f"{dept} - {behavior}", profile)
                )

        total = len(assessments)
        avg_score = sum(a["scores"]["behavior_score"] for a in assessments) / total if total else 0.0
        avg_m = sum(a["scores"]["motivation"] for a in assessments) / total if total else 0.0
        avg_a = sum(a["scores"]["ability"] for a in assessments) / total if total else 0.0
        avg_t = sum(a["scores"]["trigger"] for a in assessments) / total if total else 0.0

        if avg_score >= 70:
            dept_risk = "Low"
        elif avg_score >= 40:
            dept_risk = "Medium"
        else:
            dept_risk = "High"

        dept_results[dept] = {
            "behaviors_assessed": behaviors,
            "assessment_count": total,
            "averages": {
                "motivation": round(avg_m, 2),
                "ability": round(avg_a, 2),
                "trigger": round(avg_t, 2),
                "behavior_score": round(avg_score, 2),
            },
            "behavioral_risk": dept_risk,
        }

    return dept_results


def generate_department_recommendations(
    dept_name: str,
    dept_summary: Dict[str, Any]
) -> List[str]:

    recs: List[str] = []
    avg = dept_summary.get("averages", {})

    m = float(avg.get("motivation", 0))
    a = float(avg.get("ability", 0))
    t = float(avg.get("trigger", 0))

    recs.append(f"Department: {dept_name}")

    if a < 5:
        recs.append("- Ability is low: provide role-based training and simplified secure workflows.")
        recs.append("- Ensure password manager + MFA setup sessions are guided and supported.")

    if m < 5:
        recs.append("- Motivation is low: connect security behaviors to real business impact.")
        recs.append("- Leadership should reinforce security priorities regularly.")

    if t < 5:
        recs.append("- Triggers are weak: add reminders, phishing simulations, and just-in-time prompts.")
        recs.append("- Use checklists for high-risk actions (approvals, payments, data sharing).")

    if dept_name in ["Executives", "Finance"]:
        recs.append("- High-value target department: enforce stronger email protection and approval workflows.")
        recs.append("- Conduct tailored spear-phishing simulations and BEC drills.")

    if len(recs) == 1:
        recs.append("- Maintain current posture and continue periodic reassessment.")

    return recs


def build_org_risk_prioritization(
    prioritizer: CybersecurityRiskPrioritizer,
    departments: Dict[str, List[Dict[str, float]]]
) -> List[Dict[str, Any]]:

    common_risks = build_common_risks()

    for r in common_risks:
        for dept, profiles in departments.items():

            scenario_id = f"{r['risk_id']}-{dept.upper()}"
            scenario_name = f"{r['risk_name']} ({dept})"

            impact = float(r["impact_score"])
            if dept in ["Executives", "Finance"]:
                impact = min(10.0, impact + 0.5)

            frequency = float(r["threat_frequency"])
            if dept in ["Marketing", "HR"]:
                frequency = min(10.0, frequency + 0.5)

            prioritizer.add_risk_scenario(
                risk_id=scenario_id,
                risk_name=scenario_name,
                impact_score=impact,
                user_profiles=profiles,
                threat_frequency=frequency,
            )

    return prioritizer.prioritize_risks()


def format_report(
    dept_behavior: Dict[str, Any],
    dept_recs: Dict[str, List[str]],
    prioritized_risks: List[Dict[str, Any]]
) -> str:

    lines: List[str] = []

    lines.append("ORGANIZATIONAL SECURITY BEHAVIOR & RISK ASSESSMENT REPORT")
    lines.append("=" * 60)
    lines.append(f"Generated at: {datetime.datetime.now().isoformat()}")
    lines.append("")

    lines.append("SECTION 1: Department Behavioral Risk Summary")
    lines.append("-" * 60)

    for dept, summary in dept_behavior.items():
        avg = summary["averages"]
        lines.append(f"Department: {dept}")
        lines.append(f"  Behavioral Risk: {summary['behavioral_risk']}")
        lines.append(f"  Avg Motivation: {avg['motivation']}")
        lines.append(f"  Avg Ability: {avg['ability']}")
        lines.append(f"  Avg Trigger: {avg['trigger']}")
        lines.append(f"  Avg Behavior Score: {avg['behavior_score']}")
        lines.append("")

    lines.append("SECTION 2: Department Recommendations")
    lines.append("-" * 60)

    for dept, recs in dept_recs.items():
        for r in recs:
            lines.append(r)
        lines.append("")

    lines.append("SECTION 3: Top Prioritized Organizational Risks (Top 10)")
    lines.append("-" * 60)

    for idx, r in enumerate(prioritized_risks[:10], start=1):
        lines.append(f"{idx}. {r.get('risk_name')}")
        lines.append(f"   Priority Level: {r.get('priority_level')} | Priority Score: {r.get('priority_score')}")
        lines.append(f"   Impact: {r.get('impact_score')} | Frequency: {r.get('threat_frequency')}")
        lines.append(f"   Affected Users: {r.get('affected_users')}")
        lines.append("   Recommendations:")
        for rec in r.get("recommendations", []):
            lines.append(f"    - {rec}")
        lines.append("")

    return "\n".join(lines)


def export_json(filename: str, payload: Dict[str, Any]) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return True
    except Exception:
        return False


def main():

    fogg = FoggBehaviorModel()
    prioritizer = CybersecurityRiskPrioritizer()

    departments = build_department_profiles()

    dept_behavior = assess_department_behaviors(fogg, departments)

    dept_recs: Dict[str, List[str]] = {}
    for dept, summary in dept_behavior.items():
        dept_recs[dept] = generate_department_recommendations(dept, summary)

    prioritized_risks = build_org_risk_prioritization(prioritizer, departments)

    report_text = format_report(dept_behavior, dept_recs, prioritized_risks)
    print(report_text)

    report_payload = {
        "generated_at": datetime.datetime.now().isoformat(),
        "department_behavior_summary": dept_behavior,
        "department_recommendations": dept_recs,
        "top_10_prioritized_risks": prioritized_risks[:10],
        "all_prioritized_risks": prioritized_risks,
    }

    out_file = "org_risk_report.json"
    ok = export_json(out_file, report_payload)

    if ok:
        print(f"\nJSON report exported successfully: {out_file}")
    else:
        print("\nFailed to export JSON report.")


if __name__ == "__main__":
    main()
