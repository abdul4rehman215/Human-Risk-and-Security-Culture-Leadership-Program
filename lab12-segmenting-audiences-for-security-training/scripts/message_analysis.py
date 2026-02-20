#!/usr/bin/env python3
"""
Message Analysis Tool for Security Training
Complete implementation version
"""

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime


class MessageAnalyzer:
    def __init__(self, messages_file="aida_messages.json"):
        """Initialize message analyzer."""
        self.messages = []
        self.load_messages(messages_file)

    def load_messages(self, messages_file):
        """
        Load messages from JSON file.
        """
        try:
            with open(messages_file, "r") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.messages = data
            else:
                self.messages = []

        except FileNotFoundError:
            print(f"[ERROR] Messages file not found: {messages_file}")
            self.messages = []
        except json.JSONDecodeError:
            print(f"[ERROR] Messages file is not valid JSON: {messages_file}")
            self.messages = []
        except Exception as e:
            print(f"[ERROR] Failed to load messages: {e}")
            self.messages = []

    def analyze_message_distribution(self):
        """
        Analyze distribution of message categories.
        """
        categories = [m.get("message_category", "unknown") for m in self.messages]
        counts = Counter(categories)
        total = len(self.messages) if self.messages else 0

        print("\n=== MESSAGE CATEGORY DISTRIBUTION ===")
        for cat, c in counts.most_common():
            pct = (c / total * 100) if total else 0
            print(f"- {cat}: {c} ({pct:.1f}%)")

        return counts

    def analyze_by_department(self):
        """
        Analyze message categories by department.
        Returns: department -> category -> count
        """
        nested = defaultdict(lambda: defaultdict(int))

        for m in self.messages:
            dept = m.get("department", "Unknown")
            cat = m.get("message_category", "unknown")
            nested[dept][cat] += 1

        print("\n=== MESSAGE CATEGORIES BY DEPARTMENT ===")
        for dept in sorted(nested.keys()):
            dept_total = sum(nested[dept].values())
            print(f"\nDepartment: {dept} (Total: {dept_total})")
            for cat, c in sorted(nested[dept].items(), key=lambda x: x[1], reverse=True):
                pct = (c / dept_total * 100) if dept_total else 0
                print(f"  - {cat}: {c} ({pct:.1f}%)")

        out = {d: dict(cats) for d, cats in nested.items()}
        return out

    def analyze_risk_correlation(self):
        """
        Analyze correlation between risk scores and message categories.
        Returns: category -> risk score list
        """
        grouped = defaultdict(list)

        for m in self.messages:
            cat = m.get("message_category", "unknown")
            risk = m.get("risk_score", 0)
            try:
                risk_val = int(risk)
            except ValueError:
                risk_val = 0
            grouped[cat].append(risk_val)

        print("\n=== RISK SCORE STATISTICS BY MESSAGE CATEGORY ===")
        stats_out = {}
        for cat, scores in grouped.items():
            if not scores:
                continue
            avg = sum(scores) / len(scores)
            mn = min(scores)
            mx = max(scores)
            stats_out[cat] = {"avg": avg, "min": mn, "max": mx, "count": len(scores)}
            print(f"- {cat}: avg={avg:.2f}, min={mn}, max={mx}, count={len(scores)}")

        return grouped

    def generate_training_recommendations(self):
        """
        Generate actionable training recommendations.
        """
        recommendations = []
        total = len(self.messages)

        category_counts = self.analyze_message_distribution()
        dept_breakdown = self.analyze_by_department()
        risk_grouped = self.analyze_risk_correlation()

        def count(cat):
            return int(category_counts.get(cat, 0))

        # 1) High-risk personnel
        high_risk_count = count("high_risk_executives") + count("high_risk_it")
        if high_risk_count > 0:
            recommendations.append(
                {
                    "priority": "High",
                    "category": "High-risk personnel",
                    "count": high_risk_count,
                    "timeline": "48 hours - 7 days",
                    "recommendation": (
                        "Schedule targeted advanced training for high-risk executives and IT staff. "
                        "Include spear-phishing defense, privileged access hygiene, and incident escalation drills."
                    ),
                }
            )

        # 2) Incident history
        incident_count = count("incident_history")
        if incident_count > 0:
            recommendations.append(
                {
                    "priority": "High",
                    "category": "Incident history",
                    "count": incident_count,
                    "timeline": "72 hours",
                    "recommendation": (
                        "Assign incident refresher training immediately. "
                        "Include reporting procedure, containment steps, and scenario-based practice."
                    ),
                }
            )

        # 3) Never trained
        never_count = count("never_trained")
        if never_count > 0:
            recommendations.append(
                {
                    "priority": "Medium",
                    "category": "Never trained",
                    "count": never_count,
                    "timeline": "7 days",
                    "recommendation": (
                        "Assign onboarding security training for employees who have never trained. "
                        "Focus on basics: phishing, password security, MFA, safe browsing, and reporting."
                    ),
                }
            )

        # 4) Finance targeted training
        finance_medium = 0
        if "Finance" in dept_breakdown:
            finance_medium = int(dept_breakdown["Finance"].get("medium_risk_finance", 0))

        if finance_medium > 0:
            recommendations.append(
                {
                    "priority": "Medium",
                    "category": "Finance targeted training",
                    "count": finance_medium,
                    "timeline": "14 days",
                    "recommendation": (
                        "Deliver finance-focused modules: invoice fraud, business email compromise (BEC), "
                        "verification controls, and secure approval processes."
                    ),
                }
            )

        # 5) General refresher
        low_count = count("low_risk_general")
        if low_count > 0:
            recommendations.append(
                {
                    "priority": "Low",
                    "category": "General refresher",
                    "count": low_count,
                    "timeline": "30 days",
                    "recommendation": (
                        "Assign general security awareness refresher for low-risk personnel. "
                        "Maintain habit reinforcement: report suspicious emails, safe password practices, MFA reminders."
                    ),
                }
            )

        # 6) Risk insight
        highest_avg = None
        highest_cat = None
        for cat, scores in risk_grouped.items():
            if not scores:
                continue
            avg = sum(scores) / len(scores)
            if highest_avg is None or avg > highest_avg:
                highest_avg = avg
                highest_cat = cat

        if highest_cat is not None:
            recommendations.append(
                {
                    "priority": "Medium",
                    "category": "Risk insight",
                    "count": total,
                    "timeline": "Ongoing",
                    "recommendation": (
                        f"The category with the highest average risk score is '{highest_cat}' (avg={highest_avg:.2f}). "
                        "Review controls and training effectiveness for this group first."
                    ),
                }
            )

        return recommendations

    def export_recommendations(self, recommendations, output_file):
        """
        Export recommendations to CSV file.
        """
        fieldnames = ["priority", "category", "count", "timeline", "recommendation", "generated_at"]
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in recommendations:
                row = dict(r)
                row["generated_at"] = datetime.utcnow().isoformat() + "Z"
                writer.writerow(row)


def main():
    analyzer = MessageAnalyzer("aida_messages.json")

    if not analyzer.messages:
        print("No messages loaded. Ensure aida_messages.json exists by running aida_messaging.py first.")
        return

    analyzer.analyze_message_distribution()
    analyzer.analyze_by_department()
    analyzer.analyze_risk_correlation()

    recommendations = analyzer.generate_training_recommendations()

    out_csv = "training_recommendations.csv"
    analyzer.export_recommendations(recommendations, out_csv)

    print("\n=== TRAINING RECOMMENDATIONS SUMMARY ===")
    print(f"Total recommendations generated: {len(recommendations)}")
    print(f"Saved recommendations CSV: {out_csv}\n")

    for r in recommendations:
        print(f"- [{r['priority']}] {r['category']} | Count={r['count']} | Timeline={r['timeline']}")
        print(f"  {r['recommendation']}\n")


if __name__ == "__main__":
    main()
