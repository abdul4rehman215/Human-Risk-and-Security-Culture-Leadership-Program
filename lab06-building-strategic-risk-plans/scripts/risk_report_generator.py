#!/usr/bin/env python3
"""
Risk Management Report Generator
I will create comprehensive risk reports
"""

import pandas as pd
import json
from datetime import datetime
from typing import Any, Dict, List


class RiskReportGenerator:
    def __init__(self):
        self.report_sections = []
        self.alignment_df = None
        self.role_df = None
        self.action_plan = None

    def load_data(self):
        """Load all assessment and framework data."""
        # Load risk_alignment_matrix.csv
        self.alignment_df = pd.read_csv("risk_alignment_matrix.csv")

        # Load role_based_risk_assessment.csv
        self.role_df = pd.read_csv("role_based_risk_assessment.csv")

        # Load prioritized_action_plan.json
        with open("prioritized_action_plan.json", "r", encoding="utf-8") as f:
            self.action_plan = json.load(f)

        return True

    def generate_executive_summary(self):
        """Generate executive summary section."""
        # Calculate totals
        total_risks_assessed = int(len(self.role_df))
        critical_priorities = int((self.role_df["priority_level"] == "critical").sum())
        high_priorities = int((self.role_df["priority_level"] == "high").sum())

        # Identify top 3 risk areas by average risk_score
        top_risk_areas = (
            self.role_df.groupby("risk_type")["risk_score"]
            .mean()
            .sort_values(ascending=False)
            .head(3)
            .index
            .tolist()
        )

        # Identify top 3 most vulnerable roles by average risk_score
        most_vulnerable_roles = (
            self.role_df.groupby("role")["risk_score"]
            .mean()
            .sort_values(ascending=False)
            .head(3)
            .index
            .tolist()
        )

        # Recommended immediate actions: from action plan items with critical/high
        immediate_actions = []
        plan = self.action_plan.get("action_plan", [])
        for item in plan:
            if item.get("priority_level") in ["critical", "high"]:
                # include top mitigation strategies (up to 3 per item)
                for s in item.get("mitigation_strategies", [])[:3]:
                    immediate_actions.append(f"[{item.get('priority_level')}] {s}")

        # de-duplicate while preserving order
        seen = set()
        immediate_actions_uniq = []
        for a in immediate_actions:
            if a not in seen:
                seen.add(a)
                immediate_actions_uniq.append(a)

        summary = {
            "report_date": datetime.now().isoformat(),
            "total_risks_assessed": total_risks_assessed,
            "critical_priorities": critical_priorities,
            "high_priorities": high_priorities,
            "top_risk_areas": top_risk_areas,
            "most_vulnerable_roles": most_vulnerable_roles,
            "recommended_immediate_actions": immediate_actions_uniq[:10],
        }
        return summary

    def generate_detailed_findings(self):
        """Generate detailed findings section."""
        # Summarize alignment data
        alignment_summary = {
            "total_scenarios": int(len(self.alignment_df)),
            "status_distribution": self.alignment_df["alignment_status"].value_counts().to_dict(),
            "avg_risk_score": float(self.alignment_df["risk_score"].mean()),
        }

        # Summarize role assessment
        role_summary = {
            "total_role_risk_entries": int(len(self.role_df)),
            "avg_role_risk_score": float(self.role_df["risk_score"].mean()),
            "top_risk_types_by_score": (
                self.role_df.groupby("risk_type")["risk_score"]
                .mean()
                .sort_values(ascending=False)
                .head(5)
                .to_dict()
            ),
            "top_roles_by_score": (
                self.role_df.groupby("role")["risk_score"]
                .mean()
                .sort_values(ascending=False)
                .head(5)
                .to_dict()
            ),
        }

        # Priority breakdown
        priority_breakdown = self.role_df["priority_level"].value_counts().to_dict()

        # Culture impact analysis: average risk_score by culture_score and risk_type from alignment
        culture_impact = (
            self.alignment_df.groupby(["risk_type", "culture_score"])["risk_score"]
            .mean()
            .reset_index()
        )
        # convert to nested dict risk_type -> culture_score -> avg risk
        culture_dict: Dict[str, Dict[str, float]] = {}
        for _, row in culture_impact.iterrows():
            rt = str(row["risk_type"])
            cs = str(row["culture_score"])
            culture_dict.setdefault(rt, {})[cs] = float(row["risk_score"])

        findings = {
            "risk_behavior_alignment": alignment_summary,
            "role_risk_analysis": role_summary,
            "priority_breakdown": priority_breakdown,
            "culture_impact_analysis": culture_dict,
        }
        return findings

    def generate_recommendations(self):
        """Generate recommendations section."""
        recommendations: List[Dict[str, Any]] = []

        plan = self.action_plan.get("action_plan", [])
        for item in plan:
            recommendations.append({
                "priority_level": item.get("priority_level"),
                "timeline": item.get("timeline"),
                "average_risk_score": item.get("average_risk_score"),
                "focus_roles": item.get("top_roles"),
                "focus_risks": item.get("top_risks"),
                "mitigation_strategies": item.get("mitigation_strategies"),
                "resource_estimate": self._resource_estimate(item.get("priority_level")),
            })

        return recommendations

    def _resource_estimate(self, priority_level: str) -> str:
        if priority_level == "critical":
            return "High (dedicated team, immediate budget allocation)"
        if priority_level == "high":
            return "Medium-High (cross-team support, accelerated changes)"
        if priority_level == "medium":
            return "Medium (planned workstream)"
        return "Low (routine improvements)"

    def save_report(self, output_file="risk_management_report.json"):
        """Save complete report to JSON file."""
        report = {
            "executive_summary": self.generate_executive_summary(),
            "detailed_findings": self.generate_detailed_findings(),
            "recommendations": self.generate_recommendations(),
            "generated_at": datetime.now().isoformat(),
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"[INFO] JSON report saved: {output_file}")
        return True

    def generate_markdown_report(self, output_file="risk_report.md"):
        """Generate human-readable markdown report."""
        summary = self.generate_executive_summary()
        findings = self.generate_detailed_findings()
        recs = self.generate_recommendations()

        md = []
        md.append("# Risk Management Report")
        md.append("")
        md.append(f"**Generated:** {datetime.now().isoformat()}")
        md.append("")
        md.append("## Executive Summary")
        md.append(f"- Total risks assessed: **{summary['total_risks_assessed']}**")
        md.append(f"- Critical priorities: **{summary['critical_priorities']}**")
        md.append(f"- High priorities: **{summary['high_priorities']}**")
        md.append("")
        md.append("**Top Risk Areas (Top 3):**")
        for r in summary["top_risk_areas"]:
            md.append(f"- {r}")
        md.append("")
        md.append("**Most Vulnerable Roles (Top 3):**")
        for r in summary["most_vulnerable_roles"]:
            md.append(f"- {r}")
        md.append("")
        md.append("**Recommended Immediate Actions:**")
        for a in summary["recommended_immediate_actions"]:
            md.append(f"- {a}")
        md.append("")

        md.append("## Detailed Findings")
        md.append("### Risk-Behavior-Culture Alignment")
        md.append(f"- Total scenarios: {findings['risk_behavior_alignment']['total_scenarios']}")
        md.append(f"- Average risk score: {round(findings['risk_behavior_alignment']['avg_risk_score'], 3)}")
        md.append("- Status distribution:")
        for k, v in findings["risk_behavior_alignment"]["status_distribution"].items():
            md.append(f"  - {k}: {v}")
        md.append("")

        md.append("### Role Risk Analysis (Top 5)")
        md.append("**Top Risk Types by Average Score:**")
        for k, v in findings["role_risk_analysis"]["top_risk_types_by_score"].items():
            md.append(f"- {k}: {round(v, 2)}")
        md.append("")
        md.append("**Top Roles by Average Score:**")
        for k, v in findings["role_risk_analysis"]["top_roles_by_score"].items():
            md.append(f"- {k}: {round(v, 2)}")
        md.append("")

        md.append("### Priority Breakdown")
        for k, v in findings["priority_breakdown"].items():
            md.append(f"- {k}: {v}")
        md.append("")

        md.append("## Recommendations")
        for idx, r in enumerate(recs, start=1):
            md.append(f"### {idx}. Priority: {r['priority_level']} (Timeline: {r['timeline']})")
            md.append(f"- Average risk score: {r['average_risk_score']}")
            md.append(f"- Resource estimate: {r['resource_estimate']}")
            md.append(f"- Focus roles: {', '.join(r.get('focus_roles', []))}")
            md.append(f"- Focus risks: {', '.join(r.get('focus_risks', []))}")
            md.append("- Mitigation strategies:")
            for s in r.get("mitigation_strategies", []):
                md.append(f"  - {s}")
            md.append("")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        print(f"[INFO] Markdown report saved: {output_file}")
        return True


def main():
    print("=== Generating Risk Management Report ===")

    generator = RiskReportGenerator()
    generator.load_data()
    generator.save_report("risk_management_report.json")
    generator.generate_markdown_report("risk_report.md")

    print("[INFO] Report generation complete.")
    print("[INFO] Generated:")
    print(" - risk_management_report.json")
    print(" - risk_report.md")


if __name__ == "__main__":
    main()
