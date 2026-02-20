#!/usr/bin/env python3
"""
Security Culture Assessment Analyzer
Full Implementation (All TODOs completed)
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Import config (weights, thresholds, metadata)
from config import CATEGORY_WEIGHTS, MATURITY_THRESHOLDS, ASSESSMENT_CONFIG


class SecurityCultureAssessment:
    def __init__(self, data_dir="data", reports_dir="reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)

        # Load weights from config
        self.weights = CATEGORY_WEIGHTS

    def load_data(self, filename):
        """
        Load JSON data file
        Returns: dict or list; empty dict/list if missing
        """
        file_path = self.data_dir / filename
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[!] Warning: Missing file {file_path}, using empty dataset")
            return [] if filename == "survey_responses.json" else {}
        except json.JSONDecodeError:
            print(f"[!] Warning: Invalid JSON in {file_path}, using empty dataset")
            return [] if filename == "survey_responses.json" else {}

    @staticmethod
    def _clamp(value, low=0.0, high=100.0):
        return max(low, min(high, float(value)))

    def calculate_awareness_score(self, training_data, phishing_data):
        """
        Awareness maturity score (0-100)

        Formula:
        training_component = (completion_rate * 0.5 + average_score * 0.5)
        phishing_resilience = 100 - click_rate
        total = (training_component * 0.4) + (phishing_resilience * 0.6)
        """
        completion_rate = float(training_data.get("completion_rate", 0.0))
        average_score = float(training_data.get("average_score", 0.0))

        click_rate = float(phishing_data.get("click_rate", 100.0))
        phishing_resilience = 100.0 - click_rate

        training_component = (completion_rate * 0.5) + (average_score * 0.5)

        score = (training_component * 0.4) + (phishing_resilience * 0.6)
        score = self._clamp(score)

        return round(score, 2)

    def calculate_behavior_score(self, incident_data, compliance_data):
        """
        Behavior maturity score (0-100)
        """
        self_reporting_rate = float(incident_data.get("self_reporting_rate", 0.0))
        resolution_rate = float(incident_data.get("resolution_rate", 0.0))
        incident_effectiveness = (self_reporting_rate * 0.6) + (resolution_rate * 0.4)

        policy_compliance_rate = float(compliance_data.get("policy_compliance_rate", 0.0))
        security_practices_score = float(compliance_data.get("security_practices_score", 0.0))
        compliance_effectiveness = (policy_compliance_rate * 0.6) + (security_practices_score * 0.4)

        score = (incident_effectiveness * 0.5) + (compliance_effectiveness * 0.5)
        score = self._clamp(score)

        return round(score, 2)

    def calculate_culture_score(self, culture_data, survey_responses):
        """
        Culture maturity score (0-100)
        """
        leadership_support = float(culture_data.get("leadership_support_score", 0.0))
        employee_engagement = float(culture_data.get("employee_engagement_score", 0.0))
        communication = float(culture_data.get("communication_score", 0.0))

        leadership_avg = np.mean(
            [leadership_support, employee_engagement, communication]
        ) if any([leadership_support, employee_engagement, communication]) else 0.0

        ratings = []
        for resp in (survey_responses or []):
            answers = resp.get("answers", {})
            for _, rating in answers.items():
                try:
                    ratings.append(int(rating))
                except Exception:
                    pass

        if ratings:
            avg_rating = float(np.mean(ratings))
            survey_score = (avg_rating / 5.0) * 100.0
        else:
            survey_score = 0.0

        score = (leadership_avg * 0.6) + (survey_score * 0.4)
        score = self._clamp(score)

        return round(score, 2)

    def calculate_outcomes_score(self, incident_data):
        """
        Outcomes maturity score (0-100)
        """
        resolution_rate = float(incident_data.get("resolution_rate", 0.0))
        response_time = float(incident_data.get("average_response_time_hours", 48.0))

        response_time_score = 100.0 - ((response_time / 48.0) * 100.0)
        response_time_score = self._clamp(response_time_score)

        score = (resolution_rate * 0.6) + (response_time_score * 0.4)
        score = self._clamp(score)

        return round(score, 2)

    def determine_maturity_level(self, overall_score):
        """
        Determine maturity level based on MATURITY_THRESHOLDS config
        """
        score = float(overall_score)
        for level, (min_s, max_s) in MATURITY_THRESHOLDS.items():
            if min_s <= score <= max_s:
                return level
        return "Unknown"

    def generate_recommendations(self, scores, maturity_level):
        """
        Create recommendations based on category scores + maturity level
        """
        recommendations = []

        for category, score in scores.items():
            if score < 70:
                if score < 55:
                    priority = "High"
                elif score < 65:
                    priority = "Medium"
                else:
                    priority = "Low"

                if category == "awareness":
                    text = (
                        "Increase training completion rates, improve knowledge scores, "
                        "and reduce phishing click rates through targeted simulations."
                    )
                elif category == "behavior":
                    text = (
                        "Improve reporting culture and reinforce policy compliance "
                        "through manager-led reinforcement."
                    )
                elif category == "culture":
                    text = (
                        "Strengthen leadership messaging and increase engagement campaigns "
                        "to reinforce security as a shared value."
                    )
                elif category == "outcomes":
                    text = (
                        "Reduce incident response times and improve resolution consistency "
                        "via process automation and tabletop exercises."
                    )
                else:
                    text = "Implement targeted improvement initiatives."

                recommendations.append({
                    "category": category,
                    "priority": priority,
                    "current_score": score,
                    "recommendation": text
                })

        maturity_actions = {
            "Initial": [
                "Establish baseline metrics and mandatory awareness training."
            ],
            "Developing": [
                "Introduce department-level security champions and quarterly surveys."
            ],
            "Defined": [
                "Integrate security metrics into leadership KPIs."
            ],
            "Managed": [
                "Automate monitoring dashboards and benchmark across departments."
            ],
            "Optimizing": [
                "Implement predictive analytics and continuous adaptive learning paths."
            ]
        }

        for action in maturity_actions.get(maturity_level, []):
            recommendations.append({
                "category": "overall",
                "priority": "Strategic",
                "current_score": None,
                "recommendation": action
            })

        priority_order = {"High": 1, "Medium": 2, "Low": 3, "Strategic": 4}
        recommendations.sort(key=lambda r: priority_order.get(r["priority"], 99))

        return recommendations

    def perform_assessment(self):
        """
        Execute complete assessment
        """
        print("Loading assessment data...")

        training_data = self.load_data("training_metrics.json")
        phishing_data = self.load_data("phishing_metrics.json")
        incident_data = self.load_data("incident_metrics.json")
        compliance_data = self.load_data("compliance_metrics.json")
        culture_data = self.load_data("culture_metrics.json")
        survey_responses = self.load_data("survey_responses.json")

        print("Calculating category scores...")

        awareness_score = self.calculate_awareness_score(training_data, phishing_data)
        behavior_score = self.calculate_behavior_score(incident_data, compliance_data)
        culture_score = self.calculate_culture_score(culture_data, survey_responses)
        outcomes_score = self.calculate_outcomes_score(incident_data)

        category_scores = {
            "awareness": awareness_score,
            "behavior": behavior_score,
            "culture": culture_score,
            "outcomes": outcomes_score
        }

        overall_score = 0.0
        for cat, score in category_scores.items():
            overall_score += float(score) * float(self.weights.get(cat, 0.0))

        overall_score = round(self._clamp(overall_score), 2)

        maturity_level = self.determine_maturity_level(overall_score)
        recommendations = self.generate_recommendations(category_scores, maturity_level)

        results = {
            "assessment_date": datetime.now().isoformat(),
            "assessment_metadata": ASSESSMENT_CONFIG,
            "weights": self.weights,
            "category_scores": category_scores,
            "overall_score": overall_score,
            "maturity_level": maturity_level,
            "recommendations": recommendations
        }

        output_file = self.reports_dir / "assessment_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"[+] Saved assessment results to {output_file}")

        return results


if __name__ == "__main__":
    assessor = SecurityCultureAssessment()
    results = assessor.perform_assessment()
    print(f"\nAssessment complete: {results['maturity_level']} ({results['overall_score']}%)")
