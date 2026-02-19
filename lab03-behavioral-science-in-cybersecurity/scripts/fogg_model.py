#!/usr/bin/env python3
"""
B.J. Fogg Behavior Model Implementation for Cybersecurity
Students: Complete the TODO sections to implement the model
"""

import json
import datetime
from typing import Dict, List, Any


class FoggBehaviorModel:
    """
    Implementation of B.J. Fogg's Behavior Model for cybersecurity contexts
    """

    def __init__(self):
        self.behavior_history: List[Dict[str, Any]] = []

    def calculate_behavior_score(self, motivation: float, ability: float, trigger: float) -> float:
        """
        Calculate behavior likelihood based on Fogg's B=MAT model

        Args:
            motivation: Motivation level (0-10)
            ability: Ability level (0-10)
            trigger: Trigger strength (0-10)

        Returns:
            Behavior likelihood score (0-100)
        """

        # Normalize inputs to 0-1 range (clamp between 0-10, divide by 10)
        def clamp_0_10(x: float) -> float:
            if x < 0:
                return 0.0
            if x > 10:
                return 10.0
            return float(x)

        m = clamp_0_10(motivation) / 10.0
        a = clamp_0_10(ability) / 10.0
        t = clamp_0_10(trigger) / 10.0

        # Calculate behavior score using formula: (m * a * t) * 100
        score = (m * a * t) * 100.0

        # Return rounded score (2 decimal places)
        return round(score, 2)

    def assess_cybersecurity_behavior(self, behavior_name: str, user_profile: Dict) -> Dict:
        """
        Assess a specific cybersecurity behavior using the Fogg model

        Args:
            behavior_name: Name of the cybersecurity behavior
            user_profile: Dictionary with 'motivation', 'ability', 'trigger' keys

        Returns:
            Assessment dictionary with scores, likelihood, risk_level, recommendations
        """

        motivation = float(user_profile.get("motivation", 5))
        ability = float(user_profile.get("ability", 5))
        trigger = float(user_profile.get("trigger", 5))

        behavior_score = self.calculate_behavior_score(motivation, ability, trigger)

        if behavior_score >= 70:
            likelihood = "High"
            risk_level = "Low"
        elif behavior_score >= 40:
            likelihood = "Medium"
            risk_level = "Medium"
        else:
            likelihood = "Low"
            risk_level = "High"

        recommendations = self._generate_recommendations(motivation, ability, trigger)

        assessment = {
            "timestamp": datetime.datetime.now().isoformat(),
            "behavior_name": behavior_name,
            "scores": {
                "motivation": round(motivation, 2),
                "ability": round(ability, 2),
                "trigger": round(trigger, 2),
                "behavior_score": behavior_score,
            },
            "likelihood": likelihood,
            "risk_level": risk_level,
            "recommendations": recommendations,
        }

        self.behavior_history.append(assessment)
        return assessment

    def _generate_recommendations(self, motivation: float, ability: float, trigger: float) -> List[str]:
        """
        Generate recommendations based on Fogg model component scores
        """

        recommendations: List[str] = []

        if motivation < 5:
            recommendations.append(
                "Increase motivation via targeted security awareness campaigns and real incident examples."
            )
            recommendations.append(
                "Share success stories and measurable impact of secure behaviors to build personal relevance."
            )
            recommendations.append(
                "Implement recognition or reward programs for consistent secure behavior (positive reinforcement)."
            )

        if ability < 5:
            recommendations.append(
                "Improve ability through hands-on training and short practical exercises."
            )
            recommendations.append(
                "Provide simplified tools (password managers, MFA apps) and step-by-step documentation."
            )
            recommendations.append(
                "Reduce friction: standardize secure configurations and automate difficult security tasks where possible."
            )

        if trigger < 5:
            recommendations.append(
                "Strengthen triggers with automated reminders (email prompts, in-app alerts, scheduled nudges)."
            )
            recommendations.append(
                "Add environmental cues: posters, login banners, browser warnings, and security prompts at decision points."
            )
            recommendations.append(
                "Use regular check-ins: team huddles, security champions, and periodic simulations to reinforce behavior."
            )

        if not recommendations:
            recommendations.append(
                "Current Motivation, Ability, and Trigger levels are strong. Maintain with periodic refreshers and monitoring."
            )

        return recommendations

    def get_behavior_trends(self) -> Dict:
        """
        Analyze trends in behavior assessments over time
        """

        if not self.behavior_history:
            return {"message": "No behavior data available"}

        total = len(self.behavior_history)

        avg_m = sum(item["scores"]["motivation"] for item in self.behavior_history) / total
        avg_a = sum(item["scores"]["ability"] for item in self.behavior_history) / total
        avg_t = sum(item["scores"]["trigger"] for item in self.behavior_history) / total
        avg_b = sum(item["scores"]["behavior_score"] for item in self.behavior_history) / total

        risk_distribution = {"High": 0, "Medium": 0, "Low": 0}
        for item in self.behavior_history:
            rl = item.get("risk_level", "Medium")
            if rl == "High":
                risk_distribution["High"] += 1
            elif rl == "Low":
                risk_distribution["Low"] += 1
            else:
                risk_distribution["Medium"] += 1

        return {
            "total_assessments": total,
            "averages": {
                "motivation": round(avg_m, 2),
                "ability": round(avg_a, 2),
                "trigger": round(avg_t, 2),
                "behavior_score": round(avg_b, 2),
            },
            "risk_distribution": risk_distribution,
        }

    def export_data(self, filename: str) -> bool:
        """
        Export behavior history to JSON file
        """

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.behavior_history, f, indent=2)
            return True
        except Exception:
            return False


# Test your implementation
if __name__ == "__main__":
    fogg = FoggBehaviorModel()

    user1 = {"motivation": 7, "ability": 4, "trigger": 8}
    result1 = fogg.assess_cybersecurity_behavior("Password Management", user1)
    print(f"Test 1 - Behavior Score: {result1['scores']['behavior_score']}")
    print(f"Likelihood: {result1['likelihood']}, Risk: {result1['risk_level']}")
    print(f"Recommendations: {len(result1['recommendations'])} items\n")

    user2 = {"motivation": 9, "ability": 8, "trigger": 3}
    result2 = fogg.assess_cybersecurity_behavior("Phishing Awareness", user2)
    print(f"Test 2 - Behavior Score: {result2['scores']['behavior_score']}")
    print(f"Likelihood: {result2['likelihood']}, Risk: {result2['risk_level']}")

    trends = fogg.get_behavior_trends()
    print(f"\nTrends: {trends}")
