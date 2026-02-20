#!/usr/bin/env python3
"""
Generate presentation-ready summary
Full Implementation (All TODOs completed)
"""

import json
from pathlib import Path
from datetime import datetime


class PresentationGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = Path(reports_dir)
        self.results_file = self.reports_dir / "assessment_results.json"

    def load_results(self):
        """Load assessment results JSON."""
        try:
            with open(self.results_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[!] Missing results file: {self.results_file}")
            return None
        except json.JSONDecodeError:
            print(f"[!] Invalid JSON in: {self.results_file}")
            return None

    def create_slide_outline(self, results):
        """
        Create presentation slide outline
        """
        meta = results.get("assessment_metadata", {})
        scores = results.get("category_scores", {})
        maturity_level = results.get("maturity_level", "Unknown")
        overall_score = results.get("overall_score", 0.0)
        recs = results.get("recommendations", [])

        # key findings (derive from category strengths/weaknesses)
        weak = [c for c, v in scores.items() if float(v) < 70]
        strong = [c for c, v in scores.items() if float(v) >= 80]
        moderate = [c for c, v in scores.items() if 70 <= float(v) < 80]

        key_findings = []
        key_findings.append(f"Overall maturity is **{maturity_level}** with score **{overall_score}%**.")
        if strong:
            key_findings.append(f"Strongest areas: {', '.join([s.title() for s in strong])}.")
        if moderate:
            key_findings.append(f"Stable areas: {', '.join([m.title() for m in moderate])}.")
        if weak:
            key_findings.append(f"Priority improvement areas: {', '.join([w.title() for w in weak])}.")
        if not weak:
            key_findings.append("No categories are below 70% threshold (good baseline).")

        # top recommendations (prefer High then Medium then Strategic)
        priority_order = {"High": 1, "Medium": 2, "Strategic": 3, "Low": 4}
        recs_sorted = sorted(recs, key=lambda r: priority_order.get(r.get("priority", "Low"), 99))
        top_recs = recs_sorted[:5]

        outline = f"""
SECURITY CULTURE ASSESSMENT PRESENTATION
=========================================
SLIDE 1: Title Slide
- Security Culture Program Assessment
- Assessment Period: {meta.get('assessment_period', 'N/A')}
- Organization: {meta.get('organization', 'N/A')}
- Presented by: [YOUR NAME]

SLIDE 2: Assessment Overview
- Methodology and approach (quantitative scoring)
- Four assessment categories: Awareness, Behavior, Culture, Outcomes
- Maturity scoring framework (0-100 scale + maturity levels)

SLIDE 3: Overall Results
- Overall Score: {overall_score}%
- Maturity Level: {maturity_level}
- Snapshot date: {datetime.now().strftime('%Y-%m-%d')}

SLIDE 4: Category Breakdown
- Awareness: {scores.get('awareness', 0.0):.2f}%
- Behavior: {scores.get('behavior', 0.0):.2f}%
- Culture: {scores.get('culture', 0.0):.2f}%
- Outcomes: {scores.get('outcomes', 0.0):.2f}%
- Interpretation: highlight strongest + weakest category

SLIDE 5: Key Findings
"""
        for i, kf in enumerate(key_findings[:5], 1):
            outline += f"- {kf}\n"

        outline += """
SLIDE 6: Recommendations
"""
        if not top_recs:
            outline += "- No recommendations generated.\n"
        else:
            for r in top_recs:
                outline += f"- [{r.get('priority')}] {r.get('category').title()}: {r.get('recommendation')}\n"

        outline += """
SLIDE 7: Next Steps
- Immediate actions (0-3 months): Fix weak categories and close gaps <70%
- Short-term initiatives (3-6 months): role-based training + manager reinforcement
- Long-term goals (6-12 months): automate metrics and build continuous monitoring

SLIDE 8: Questions
- Contact information
- Additional resources
"""
        return outline.strip() + "\n"

    def generate_talking_points(self, results):
        """
        Generate speaker notes for presentation
        """
        meta = results.get("assessment_metadata", {})
        scores = results.get("category_scores", {})
        maturity_level = results.get("maturity_level", "Unknown")
        overall_score = results.get("overall_score", 0.0)
        recs = results.get("recommendations", [])

        # pick top 3 by priority
        priority_order = {"High": 1, "Medium": 2, "Strategic": 3, "Low": 4}
        recs_sorted = sorted(recs, key=lambda r: priority_order.get(r.get("priority", "Low"), 99))
        top3 = recs_sorted[:3]

        tp = "PRESENTATION TALKING POINTS\n"
        tp += "=" * 60 + "\n\n"

        tp += "SLIDE 1 (Title)\n"
        tp += "- Introduce the goal: assess current security culture maturity using measurable metrics.\n"
        tp += f"- Period: {meta.get('assessment_period', 'N/A')} | Organization: {meta.get('organization', 'N/A')}\n\n"

        tp += "SLIDE 2 (Overview)\n"
        tp += "- We scored maturity across 4 categories using quantitative indicators.\n"
        tp += "- Scores range 0–100 and are mapped to maturity levels (Initial → Optimizing).\n\n"

        tp += "SLIDE 3 (Overall Results)\n"
        tp += f"- Overall maturity: {maturity_level}.\n"
        tp += f"- Overall score: {overall_score}%.\n"
        tp += "- This score reflects weighted performance across all categories.\n\n"

        tp += "SLIDE 4 (Category Breakdown)\n"
        tp += f"- Awareness: {scores.get('awareness', 0.0):.2f}% (training + phishing resilience)\n"
        tp += f"- Behavior: {scores.get('behavior', 0.0):.2f}% (reporting + compliance)\n"
        tp += f"- Culture: {scores.get('culture', 0.0):.2f}% (leadership + engagement + survey sentiment)\n"
        tp += f"- Outcomes: {scores.get('outcomes', 0.0):.2f}% (response effectiveness + resolution)\n"
        tp += "- Call out strengths and the single most important gap.\n\n"

        tp += "SLIDE 5 (Key Findings)\n"
        tp += "- Translate scores into real-world meaning: what people do, what leaders reinforce, what outcomes improved.\n"
        tp += "- Emphasize that compliance is not culture; behaviors and outcomes matter.\n\n"

        tp += "SLIDE 6 (Recommendations)\n"
        if not top3:
            tp += "- No recommendations generated; we are above baseline thresholds.\n\n"
        else:
            tp += "- Top priorities:\n"
            for r in top3:
                tp += f"  * [{r.get('priority')}] {r.get('category').title()}: {r.get('recommendation')}\n"
            tp += "\n"

        tp += "SLIDE 7 (Next Steps)\n"
        tp += "- Immediate: address weak areas and standardize reporting + simulations.\n"
        tp += "- Short-term: role-based training paths + managers as multipliers.\n"
        tp += "- Long-term: automation + dashboards + quarterly reassessments.\n\n"

        tp += "SLIDE 8 (Q&A)\n"
        tp += "- Invite questions and confirm where detailed report, charts, and JSON files are stored.\n"
        tp += "- Offer follow-up plan for next quarter reassessment.\n\n"

        return tp

    def save_outputs(self, outline, talking_points):
        outline_file = self.reports_dir / "presentation_outline.txt"
        tp_file = self.reports_dir / "presentation_talking_points.txt"

        with open(outline_file, "w") as f:
            f.write(outline)

        with open(tp_file, "w") as f:
            f.write(talking_points)

        print(f"[+] Saved: {outline_file}")
        print(f"[+] Saved: {tp_file}")

    def run(self):
        results = self.load_results()
        if not results:
            print("[!] Cannot generate presentation materials without assessment_results.json")
            return

        outline = self.create_slide_outline(results)
        talking_points = self.generate_talking_points(results)
        self.save_outputs(outline, talking_points)

        print("\n--- Presentation Outline Preview (first 30 lines) ---")
        print("\n".join(outline.splitlines()[:30]))
        print("... (preview truncated) ...")


if __name__ == "__main__":
    generator = PresentationGenerator()
    generator.run()
