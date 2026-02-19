#!/usr/bin/env python3
# (Generates samm_report.txt + samm_report.html dashboard-style)

"""
SAMM Report Generator
Students: Create comprehensive HTML/PDF reports from assessment results
"""

import json
from datetime import datetime
import sys
import os


class SAMMReportGenerator:
    def __init__(self):
        self.assessment_results = None
        self.analysis_results = None

    def load_results(self, assessment_file, analysis_file):
        """
        Load assessment and analysis results.

        Args:
            assessment_file: Path to assessment results JSON
            analysis_file: Path to analysis results JSON

        Returns:
            Boolean indicating success
        """
        try:
            with open(assessment_file, "r", encoding="utf-8") as f:
                self.assessment_results = json.load(f)
            with open(analysis_file, "r", encoding="utf-8") as f:
                self.analysis_results = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading results: {e}")
            return False

    def generate_executive_summary(self):
        """
        Generate executive summary section.

        Returns:
            String containing formatted executive summary
        """
        overall = self.assessment_results.get("overall", {})
        level = overall.get("maturity_level", {})
        score = overall.get("weighted_score", 0)

        categories = self.assessment_results.get("categories", {})
        # strengths = top 2 categories by score
        sorted_cats = sorted(categories.items(), key=lambda x: x[1].get("score", 0), reverse=True)
        strengths = sorted_cats[:2]
        weaknesses = sorted_cats[-2:] if len(sorted_cats) >= 2 else sorted_cats

        lines = []
        lines.append(f"Overall SAMM Maturity Score: {score}")
        lines.append(f"Overall Maturity Level: {level.get('level')} - {level.get('name')}")
        lines.append("")
        lines.append("Key Strengths:")
        for k, v in strengths:
            lines.append(f"- {v.get('name')}: {v.get('score')}")
        lines.append("")
        lines.append("Key Weaknesses:")
        for k, v in weaknesses:
            lines.append(f"- {v.get('name')}: {v.get('score')}")

        return "\n".join(lines)

    def generate_category_details(self):
        """
        Generate detailed category analysis.

        Returns:
            String containing formatted category details
        """
        categories = self.assessment_results.get("categories", {})
        lines = []
        for cat_key, cat_val in categories.items():
            lvl = cat_val.get("maturity_level", {})
            lines.append(f"Category: {cat_val.get('name')}")
            lines.append(f"  Score: {cat_val.get('score')} (Weight: {cat_val.get('weight')})")
            lines.append(f"  Maturity Level: {lvl.get('level')} - {lvl.get('name')}")
            lines.append("  Recommendations:")
            for r in cat_val.get("recommendations", []):
                lines.append(f"   - {r}")
            lines.append("")
        return "\n".join(lines)

    def generate_recommendations_section(self):
        """
        Generate prioritized recommendations.

        Returns:
            String containing formatted recommendations
        """
        categories = self.assessment_results.get("categories", {})
        all_recs = []

        # collect recs with category + score (lower score -> higher priority)
        for cat_key, cat_val in categories.items():
            score = float(cat_val.get("score", 0))
            for rec in cat_val.get("recommendations", []):
                all_recs.append((score, cat_val.get("name"), rec))

        # prioritize based on low score first
        all_recs.sort(key=lambda x: x[0])

        lines = []
        lines.append("Prioritized Recommendations (lowest scoring categories first)")
        lines.append("-" * 55)

        for idx, (score, cat_name, rec) in enumerate(all_recs, start=1):
            # simple impact/effort labeling
            impact = "High" if score < 2.5 else ("Medium" if score < 3.5 else "Low")
            effort = "Medium"
            lines.append(f"{idx}. [{cat_name}] (Impact: {impact}, Effort: {effort}) {rec}")

        return "\n".join(lines)

    def generate_html_report(self, output_file):
        """
        Generate complete HTML report.

        Args:
            output_file: Path to output HTML file

        Returns:
            Boolean indicating success
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            exec_summary = self.generate_executive_summary()
            cat_details = self.generate_category_details()
            recs = self.generate_recommendations_section()

            # Visualizations from analysis_results
            plots = self.analysis_results.get("plots", {})

            # Create HTML structure with CSS styling
            html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>SAMM Security Awareness Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }}
    h1 {{ color: #222; }}
    h2 {{ margin-top: 30px; }}
    .section {{ background: #f7f7f7; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
    pre {{ white-space: pre-wrap; word-wrap: break-word; background: #fff; padding: 10px; border-radius: 6px; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px; margin: 10px 0; }}
    .meta {{ color: #555; font-size: 14px; }}
  </style>
</head>
<body>
  <h1>SAMM Security Awareness Maturity Report</h1>
  <p class="meta">Generated: {datetime.now().isoformat()}</p>

  <div class="section">
    <h2>Executive Summary</h2>
    <pre>{exec_summary}</pre>
  </div>

  <div class="section">
    <h2>Category Details</h2>
    <pre>{cat_details}</pre>
  </div>

  <div class="section">
    <h2>Visualizations</h2>
    <p>These charts are generated by the data analysis module.</p>
"""

            # Embed images if they exist
            # Use relative paths for browser convenience
            for k, path in plots.items():
                rel_path = os.path.basename(path)
                html += f"<h3>{k}</h3>\n"
                html += f'<img src="{rel_path}" alt="{k}">\n'

            html += f"""
  </div>

  <div class="section">
    <h2>Recommendations</h2>
    <pre>{recs}</pre>
  </div>

</body>
</html>
"""

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)

            return True
        except Exception as e:
            print(f"Error generating HTML report: {e}")
            return False

    def generate_text_report(self, output_file):
        """
        Generate plain text report.

        Args:
            output_file: Path to output text file

        Returns:
            Boolean indicating success
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            exec_summary = self.generate_executive_summary()
            cat_details = self.generate_category_details()
            recs = self.generate_recommendations_section()

            lines = []
            lines.append("SAMM SECURITY AWARENESS MATURITY REPORT")
            lines.append("=" * 45)
            lines.append(f"Generated: {datetime.now().isoformat()}")
            lines.append("")
            lines.append("EXECUTIVE SUMMARY")
            lines.append("-" * 45)
            lines.append(exec_summary)
            lines.append("")
            lines.append("CATEGORY DETAILS")
            lines.append("-" * 45)
            lines.append(cat_details)
            lines.append("")
            lines.append("PRIORITIZED RECOMMENDATIONS")
            lines.append("-" * 45)
            lines.append(recs)
            lines.append("")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            return True
        except Exception as e:
            print(f"Error generating text report: {e}")
            return False


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python3 report_generator.py <assessment_results.json> <analysis_results.json>")
        sys.exit(1)

    assessment_file = sys.argv[1]
    analysis_file = sys.argv[2]

    # Output files in same directory as input assessment file (usually ../reports)
    out_dir = os.path.dirname(os.path.abspath(assessment_file))
    text_out = os.path.join(out_dir, "samm_report.txt")
    html_out = os.path.join(out_dir, "samm_report.html")

    gen = SAMMReportGenerator()
    if not gen.load_results(assessment_file, analysis_file):
        sys.exit(1)

    ok_txt = gen.generate_text_report(text_out)
    ok_html = gen.generate_html_report(html_out)

    if ok_txt:
        print(f"Text report generated: {text_out}")
    else:
        print("Failed to generate text report.")

    if ok_html:
        print(f"HTML report generated: {html_out}")
        print("NOTE: Ensure the PNG charts exist in the same reports directory for HTML embedding.")
    else:
        print("Failed to generate HTML report.")
