#!/usr/bin/env python3
"""
Report Generation Module
"""

import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class ReportGenerator:
    def __init__(self, results: dict, org_info: dict):
        """
        Initialize report generator.

        Args:
            results: Analysis results dictionary
            org_info: Organization information
        """
        self.results = results
        self.org_info = org_info

    def generate_bar_chart(self, domain_scores: dict, output_path: str):
        """
        Generate domain scores bar chart.

        Args:
            domain_scores: Dictionary of domain scores
            output_path: Path to save chart
        """
        domains = list(domain_scores.keys())
        scores = [domain_scores[d] for d in domains]

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=domains, y=scores)
        ax.set_title("Security Domain Benchmark Scores")
        ax.set_xlabel("Domain")
        ax.set_ylabel("Score (%)")
        plt.xticks(rotation=25, ha="right")

        # Add score labels above bars
        for i, v in enumerate(scores):
            ax.text(i, v + 1, f"{v:.1f}", ha="center", fontsize=9)

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def generate_recommendations(self, domain_scores: dict) -> list:
        """
        Generate improvement recommendations.

        Args:
            domain_scores: Dictionary of domain scores

        Returns:
            List of recommendation strings
        """
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])
        lowest = sorted_domains[:2]  # Focus on bottom 2 domains

        recs = []
        for domain, score in lowest:
            gap = round(100.0 - float(score), 2)

            if domain == "governance":
                recs.append(
                    f"[{domain}] Strengthen policy documentation and executive oversight (gap {gap}%)."
                )
            elif domain == "risk_management":
                recs.append(
                    f"[{domain}] Formalize risk assessment cadence and risk treatment tracking (gap {gap}%)."
                )
            elif domain == "incident_response":
                recs.append(
                    f"[{domain}] Update IR plan, run tabletop exercises, and define IR roles (gap {gap}%)."
                )
            elif domain == "awareness":
                recs.append(
                    f"[{domain}] Expand training coverage and measure awareness outcomes (gap {gap}%)."
                )
            elif domain == "technical_controls":
                recs.append(
                    f"[{domain}] Improve control coverage and monitoring/telemetry (gap {gap}%)."
                )
            else:
                recs.append(
                    f"[{domain}] Improve this domain through controls, documentation, and measurement (gap {gap}%)."
                )

        return recs

    def generate_markdown_report(self, output_path: str):
        """
        Generate detailed markdown report.

        Args:
            output_path: Path to save report
        """
        domain_scores = self.results.get("domain_scores", {})
        overall_score = self.results.get("overall_score", 0.0)
        maturity = self.results.get("maturity_level", {})
        recs = self.generate_recommendations(domain_scores)

        md = []
        md.append("# Security Program Benchmark Assessment Report")
        md.append("")
        md.append(f"**Generated:** {datetime.now().isoformat()}")
        md.append("")
        md.append("## Organization Information")
        md.append(f"- Name: **{self.org_info.get('name', 'N/A')}**")
        md.append(f"- Industry: **{self.org_info.get('industry', 'N/A')}**")
        md.append(f"- Assessment Date: **{self.org_info.get('date', 'N/A')}**")
        md.append("")
        md.append("## Executive Summary")
        md.append(f"- Overall Score: **{overall_score:.2f}%**")
        md.append(
            f"- Maturity Level: **{maturity.get('level', 'N/A')} - {maturity.get('name', 'N/A')}**"
        )
        md.append("")
        md.append("## Domain Scores")
        md.append("")
        md.append("| Domain | Score (%) |")
        md.append("|---|---:|")

        for d, s in domain_scores.items():
            md.append(f"| {d} | {float(s):.2f} |")

        md.append("")
        md.append("## Recommendations")

        for r in recs:
            md.append(f"- {r}")

        md.append("")
        md.append("## Notes")
        md.append("- Scores are computed from weighted questions (1-5) normalized to percentages.")
        md.append("- Overall score is weighted by domain importance from the framework config.")
        md.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))
