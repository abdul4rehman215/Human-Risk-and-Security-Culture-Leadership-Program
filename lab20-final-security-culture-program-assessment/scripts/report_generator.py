#!/usr/bin/env python3
"""
Security Culture Assessment Report Generator
Full Implementation (All TODOs completed)
"""

import json
import matplotlib

matplotlib.use("Agg")  # headless safe
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

from config import MATURITY_THRESHOLDS, ASSESSMENT_CONFIG


class ReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)

    def load_results(self):
        """
        Load assessment results from JSON file
        Returns: dict or None
        """
        results_file = self.reports_dir / "assessment_results.json"
        try:
            with open(results_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[!] Error: Missing {results_file}")
            return None
        except json.JSONDecodeError:
            print(f"[!] Error: Invalid JSON in {results_file}")
            return None

    def _threshold_lines(self):
        """
        Return list of (label, yvalue) to draw maturity threshold lines.
        We'll draw lower bounds of each level for visibility.
        """
        lines = []
        for level, (min_s, max_s) in MATURITY_THRESHOLDS.items():
            # only plot the min boundary except Initial (0) to avoid clutter
            if min_s != 0:
                lines.append((level, float(min_s)))
        # sort by y
        lines.sort(key=lambda x: x[1])
        return lines

    def create_bar_chart(self, scores, output_file="maturity_scores.png"):
        """
        Create bar chart of maturity scores
        """
        categories = list(scores.keys())
        values = [float(scores[c]) for c in categories]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(categories, values)

        ax.set_title("Security Culture Maturity Scores by Category")
        ax.set_ylabel("Score (0-100)")
        ax.set_ylim(0, 100)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        # Threshold lines
        for label, y in self._threshold_lines():
            ax.axhline(y=y, linestyle="--", linewidth=1)
            ax.text(len(categories) - 0.5, y + 0.5, f"{label} ({int(y)}+)", fontsize=8)

        # Value labels
        for i, v in enumerate(values):
            ax.text(i, v + 1.2, f"{v:.1f}", ha="center", fontsize=9)

        out_path = self.reports_dir / output_file
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        print(f"[+] Saved bar chart: {out_path}")

    def create_radar_chart(self, scores, output_file="maturity_radar.png"):
        """
        Create radar chart of maturity scores
        """
        categories = list(scores.keys())
        values = [float(scores[c]) for c in categories]

        # Radar needs closed loop
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection="polar"))

        ax.plot(angles, values, linewidth=2)
        ax.fill(angles, values, alpha=0.2)

        ax.set_title("Security Culture Maturity Radar", y=1.08)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([c.title() for c in categories])
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_ylim(0, 100)

        out_path = self.reports_dir / output_file
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        print(f"[+] Saved radar chart: {out_path}")

    def generate_executive_summary(self, results):
        """
        Generate executive summary text
        """
        meta = results.get("assessment_metadata", ASSESSMENT_CONFIG)
        scores = results.get("category_scores", {})
        recommendations = results.get("recommendations", [])

        # pick top 3 actionable recs (exclude Strategic)
        actionable = [r for r in recommendations if r.get("priority") != "Strategic"]
        top3 = actionable[:3]

        summary = f"""
SECURITY CULTURE ASSESSMENT - EXECUTIVE SUMMARY
================================================
Program: {meta.get('program_name', 'N/A')}
Organization: {meta.get('organization', 'N/A')}
Assessment Period: {meta.get('assessment_period', 'N/A')}
Assessment Date: {datetime.now().strftime('%B %d, %Y')}

OVERALL RESULT
--------------
Overall Maturity Level: {results.get('maturity_level', 'Unknown')}
Overall Score: {results.get('overall_score', 0.0)}%

CATEGORY SCORES
--------------
"""

        for cat, val in scores.items():
            summary += f"- {cat.title():<10}: {val:.2f}%\n"

        summary += """
KEY FINDINGS
------------
- Category scores show strengths and weaknesses across awareness, behavior, culture, and outcomes.
- Categories under 70% indicate areas that need targeted improvement efforts.
- Higher maturity requires consistent metrics tracking and leadership reinforcement.

TOP RECOMMENDATIONS
-------------------
"""
        if not top3:
            summary += "- No critical recommendations generated (all categories above threshold).\n"
        else:
            for i, rec in enumerate(top3, 1):
                summary += f"{i}. [{rec.get('priority')}] {rec.get('category').title()}: {rec.get('recommendation')}\n"

        summary += "\n(End of Executive Summary)\n"
        return summary.strip() + "\n"

    def generate_detailed_report(self, results):
        """
        Generate comprehensive assessment report
        """
        meta = results.get("assessment_metadata", ASSESSMENT_CONFIG)
        scores = results.get("category_scores", {})
        maturity = results.get("maturity_level", "Unknown")
        overall = results.get("overall_score", 0.0)
        recs = results.get("recommendations", [])

        report = "SECURITY CULTURE ASSESSMENT - DETAILED REPORT\n"
        report += "=" * 60 + "\n\n"

        report += "1) ASSESSMENT METADATA\n"
        report += "-" * 60 + "\n"
        report += f"Program: {meta.get('program_name', 'N/A')}\n"
        report += f"Organization: {meta.get('organization', 'N/A')}\n"
        report += f"Assessment Period: {meta.get('assessment_period', 'N/A')}\n"
        report += f"Assessment Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        report += f"Assessment Version: {meta.get('assessment_version', 'N/A')}\n\n"

        report += "2) METHODOLOGY\n"
        report += "-" * 60 + "\n"
        report += (
            "This assessment calculates maturity scores across four categories:\n"
            "Awareness, Behavior, Culture, and Outcomes. Each category is scored 0-100\n"
            "using quantitative metrics (training, phishing, incidents, compliance, leadership,\n"
            "and survey sentiment). Scores are combined using configured weights to produce\n"
            "an overall maturity score and maturity level.\n\n"
        )

        report += "3) OVERALL RESULTS\n"
        report += "-" * 60 + "\n"
        report += f"Overall Score: {overall}%\n"
        report += f"Maturity Level: {maturity}\n\n"

        report += "4) CATEGORY ANALYSIS\n"
        report += "-" * 60 + "\n"
        for cat, val in scores.items():
            interpretation = (
                "Strong"
                if float(val) >= 80
                else ("Moderate" if float(val) >= 70 else "Needs Improvement")
            )
            report += f"\n{cat.upper()}:\n"
            report += f"- Score: {val:.2f}%\n"
            report += f"- Interpretation: {interpretation}\n"
            if cat == "awareness":
                report += "- Looks at training completion/quality and phishing resilience.\n"
            elif cat == "behavior":
                report += "- Looks at reporting behavior, compliance, and practical security habits.\n"
            elif cat == "culture":
                report += "- Looks at leadership support, engagement, and communication + survey sentiment.\n"
            elif cat == "outcomes":
                report += "- Looks at response effectiveness and resolution quality.\n"

        report += "\n\n5) RECOMMENDATIONS\n"
        report += "-" * 60 + "\n"
        if not recs:
            report += "No recommendations generated.\n"
        else:
            for rec in recs:
                pr = rec.get("priority", "N/A")
                cat = rec.get("category", "N/A")
                cur = rec.get("current_score", None)
                txt = rec.get("recommendation", "")
                if cur is None:
                    report += f"- [{pr}] {cat.title()}: {txt}\n"
                else:
                    report += f"- [{pr}] {cat.title()} (Current: {cur:.2f}%): {txt}\n"

        report += "\n\n6) NEXT STEPS / ACTION PLAN\n"
        report += "-" * 60 + "\n"
        report += (
            "Immediate (0-3 months):\n"
            "- Address categories below 70% with targeted training and communication\n"
            "- Improve incident reporting and reduce phishing click rate through simulations\n\n"
            "Short-term (3-6 months):\n"
            "- Introduce role-based learning paths and manager reinforcement\n"
            "- Increase leadership visibility and communication cadence\n\n"
            "Long-term (6-12 months):\n"
            "- Automate metric collection and build continuous monitoring dashboards\n"
            "- Use trend analytics to predict weak areas and intervene early\n\n"
        )

        report += "7) CONCLUSION\n"
        report += "-" * 60 + "\n"
        report += (
            "This assessment provides a quantitative snapshot of security culture maturity.\n"
            "Re-run quarterly to measure progress, validate interventions, and maintain a\n"
            "sustained improvement cycle.\n"
        )

        return report

    def generate_all_reports(self):
        print("Loading assessment results...")
        results = self.load_results()

        if not results:
            print("Error: No assessment results found")
            return

        scores = results.get("category_scores", {})

        print("Generating visualizations...")
        self.create_bar_chart(scores, "maturity_scores.png")
        self.create_radar_chart(scores, "maturity_radar.png")

        print("Generating text reports...")
        exec_summary = self.generate_executive_summary(results)
        detailed = self.generate_detailed_report(results)

        exec_file = self.reports_dir / "executive_summary.txt"
        det_file = self.reports_dir / "detailed_report.txt"

        with open(exec_file, "w") as f:
            f.write(exec_summary)

        with open(det_file, "w") as f:
            f.write(detailed)

        print(f"[+] Saved executive summary: {exec_file}")
        print(f"[+] Saved detailed report: {det_file}")
        print(f"\nReports generated in {self.reports_dir}")


if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate_all_reports()
