#!/usr/bin/env python3
"""
Kirkpatrick Four-Level Training Evaluation Implementation
Complete implementation version
"""

import os
import json
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statistics_helper import calculate_cohens_d, perform_ttest, calculate_confidence_interval
from roi_calculator import calculate_training_roi


class KirkpatrickEvaluator:
    def __init__(self, data_file, criteria_file):
        """Initialize evaluator with data and criteria."""
        self.data = pd.read_csv(data_file)

        with open(criteria_file, "r") as f:
            self.criteria = json.load(f)

        self.results = {}

    def level1_reaction(self):
        """
        Level 1: Evaluate participant reactions to training.
        """
        print("=== LEVEL 1: REACTION EVALUATION ===")

        scores = self.data["reaction_score"].astype(float)
        mean_score = float(scores.mean())
        median_score = float(scores.median())
        std_score = float(scores.std(ddof=1))

        threshold = float(self.criteria["reaction_threshold"])
        above = int((scores >= threshold).sum())
        below = int((scores < threshold).sum())
        satisfaction_percent = float((above / len(scores)) * 100) if len(scores) > 0 else 0.0

        level1 = {
            "mean_reaction_score": mean_score,
            "median_reaction_score": median_score,
            "std_reaction_score": std_score,
            "threshold": threshold,
            "participants_above_threshold": above,
            "participants_below_threshold": below,
            "satisfaction_percent": satisfaction_percent,
        }

        self.results["level1"] = level1
        return level1

    def level2_learning(self):
        """
        Level 2: Evaluate learning outcomes.
        """
        print("\n=== LEVEL 2: LEARNING EVALUATION ===")

        pre = self.data["pre_test"].astype(float)
        post = self.data["post_test"].astype(float)

        pre_avg = float(pre.mean())
        post_avg = float(post.mean())

        improvement = post - pre
        self.data["improvement"] = improvement

        improvement_avg = float(improvement.mean())
        improvement_median = float(improvement.median())

        passing_score = float(self.criteria["passing_score"])
        passing_count = int((post >= passing_score).sum())
        passing_rate = float((passing_count / len(post)) * 100) if len(post) > 0 else 0.0

        cohens_d = float(calculate_cohens_d(pre.values, post.values))
        t_stat, p_val = perform_ttest(pre.values, post.values)

        ci_low, ci_high = calculate_confidence_interval(improvement.values, confidence=0.95)

        level2 = {
            "pre_test_avg": pre_avg,
            "post_test_avg": post_avg,
            "avg_improvement": improvement_avg,
            "median_improvement": improvement_median,
            "passing_score": passing_score,
            "passing_count": passing_count,
            "passing_rate_percent": passing_rate,
            "cohens_d_effect_size": cohens_d,
            "paired_ttest_t_stat": float(t_stat),
            "paired_ttest_p_value": float(p_val),
            "improvement_mean_ci_95": {"lower": float(ci_low), "upper": float(ci_high)},
        }

        self.results["level2"] = level2
        return level2

    def level3_behavior(self):
        """
        Level 3: Evaluate behavior change.
        """
        print("\n=== LEVEL 3: BEHAVIOR EVALUATION ===")

        before = self.data["incidents_before"].astype(float)
        after = self.data["incidents_after"].astype(float)

        total_before = float(before.sum())
        total_after = float(after.sum())

        reduction = total_before - total_after
        reduction_rate = float(reduction / total_before) if total_before > 0 else 0.0

        individual_rates = []
        categories = {"high_improvement": 0, "moderate_improvement": 0, "low_or_none": 0}

        for b, a in zip(before.values, after.values):
            if b <= 0:
                rate = 0.0
            else:
                rate = (b - a) / b
            individual_rates.append(rate)

            if rate >= 0.75:
                categories["high_improvement"] += 1
            elif rate >= 0.25:
                categories["moderate_improvement"] += 1
            else:
                categories["low_or_none"] += 1

        self.data["behavior_improvement_rate"] = individual_rates

        level3 = {
            "total_incidents_before": total_before,
            "total_incidents_after": total_after,
            "total_incidents_reduced": float(reduction),
            "overall_reduction_rate": float(reduction_rate),
            "individual_improvement_rate_avg": float(np.mean(individual_rates)) if individual_rates else 0.0,
            "improvement_categories": categories,
        }

        self.results["level3"] = level3
        return level3

    def level4_results(self):
        """
        Level 4: Evaluate business results and ROI.
        """
        print("\n=== LEVEL 4: RESULTS EVALUATION ===")

        impact = self.data["business_impact"].astype(float)
        avg_impact = float(impact.mean())

        incidents_before_total = float(self.data["incidents_before"].sum())
        incidents_after_total = float(self.data["incidents_after"].sum())
        num_participants = int(len(self.data))

        roi_data = calculate_training_roi(
            incidents_before=incidents_before_total,
            incidents_after=incidents_after_total,
            num_participants=num_participants,
            incident_cost=float(self.criteria["incident_cost"]),
            cost_per_participant=float(self.criteria["training_cost_per_person"]),
        )

        level4 = {
            "avg_business_impact_score": avg_impact,
            "business_impact_threshold": float(self.criteria["business_impact_threshold"]),
            "roi": roi_data,
        }

        self.results["level4"] = level4
        return level4

    def generate_report(self):
        """
        Generate comprehensive evaluation report.
        """
        print("\n" + "=" * 60)
        print("COMPREHENSIVE EVALUATION REPORT")
        print("=" * 60)

        l1_sat = self.results.get("level1", {}).get("satisfaction_percent", 0.0)

        l2_avg_imp = self.results.get("level2", {}).get("avg_improvement", 0.0)
        l2_target = float(self.criteria["learning_improvement_target"])
        l2_score = min(100.0, (l2_avg_imp / l2_target) * 100.0) if l2_target > 0 else 0.0

        l3_rate = self.results.get("level3", {}).get("overall_reduction_rate", 0.0)
        l3_target = float(self.criteria["behavior_reduction_target"])
        l3_score = min(100.0, (l3_rate / l3_target) * 100.0) if l3_target > 0 else 0.0

        avg_impact = self.results.get("level4", {}).get("avg_business_impact_score", 0.0)
        impact_threshold = float(self.criteria["business_impact_threshold"])
        l4_score = min(100.0, (avg_impact / impact_threshold) * 100.0) if impact_threshold > 0 else 0.0

        overall_score = (0.25 * l1_sat) + (0.25 * l2_score) + (0.25 * l3_score) + (0.25 * l4_score)

        recommendations = []

        if l1_sat < 80:
            recommendations.append("Improve participant engagement to raise reaction scores above threshold.")
        if l2_avg_imp < l2_target:
            recommendations.append("Increase learning reinforcement: add practice exercises and follow-up quizzes.")
        if l3_rate < l3_target:
            recommendations.append("Strengthen behavior transfer: run phishing simulations and manager follow-ups.")
        if avg_impact < impact_threshold:
            recommendations.append("Align training more closely with business goals and measure operational impact.")
        roi_percent = self.results.get("level4", {}).get("roi", {}).get("roi_percent", 0.0)
        if roi_percent < 0:
            recommendations.append("ROI is negative: reduce costs or increase incident reduction impact.")

        summary = {
            "timestamp": datetime.now().isoformat(),
            "overall_effectiveness_score": float(overall_score),
            "level_breakdown_scores": {
                "level1_reaction_score_percent": float(l1_sat),
                "level2_learning_score_percent": float(l2_score),
                "level3_behavior_score_percent": float(l3_score),
                "level4_results_score_percent": float(l4_score),
            },
            "recommendations": recommendations,
            "detailed_results": self.results,
        }

        print(f"Overall Effectiveness Score: {overall_score:.2f}/100\n")
        print("Recommendations:")
        if recommendations:
            for r in recommendations:
                print(f"- {r}")
        else:
            print("- Training meets or exceeds all targets. Maintain and iterate improvements.")

        return summary

    def create_visualizations(self):
        """
        Create visualizations for all four levels.
        """
        os.makedirs("visualizations", exist_ok=True)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Kirkpatrick Four-Level Training Evaluation", fontsize=16)

        axes[0, 0].hist(self.data["reaction_score"].astype(float), bins=8, edgecolor="black")
        axes[0, 0].set_title("Level 1: Reaction Score Distribution")
        axes[0, 0].set_xlabel("Reaction Score")
        axes[0, 0].set_ylabel("Count")

        axes[0, 1].scatter(self.data["pre_test"].astype(float), self.data["post_test"].astype(float))
        axes[0, 1].plot([0, 100], [0, 100], linestyle="--")
        axes[0, 1].set_title("Level 2: Pre vs Post Test Scores")
        axes[0, 1].set_xlabel("Pre-test")
        axes[0, 1].set_ylabel("Post-test")

        total_before = self.data["incidents_before"].sum()
        total_after = self.data["incidents_after"].sum()
        axes[1, 0].bar(["Before", "After"], [total_before, total_after], edgecolor="black")
        axes[1, 0].set_title("Level 3: Total Incidents Before vs After")
        axes[1, 0].set_ylabel("Total Incidents")

        dept_avg = self.data.groupby("department")["business_impact"].mean().sort_values(ascending=False)
        axes[1, 1].bar(dept_avg.index.astype(str), dept_avg.values, edgecolor="black")
        axes[1, 1].set_title("Level 4: Avg Business Impact by Department")
        axes[1, 1].set_xlabel("Department")
        axes[1, 1].set_ylabel("Avg Business Impact")
        axes[1, 1].tick_params(axis="x", rotation=30)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        out_file = f"visualizations/kirkpatrick_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(out_file)
        plt.close(fig)

        print(f"\nVisualization saved to: {out_file}")
        return out_file


def main():
    evaluator = KirkpatrickEvaluator("data/training_data.csv", "data/criteria.json")

    evaluator.level1_reaction()
    evaluator.level2_learning()
    evaluator.level3_behavior()
    evaluator.level4_results()

    summary = evaluator.generate_report()

    viz_file = evaluator.create_visualizations()
    summary["visualization_file"] = viz_file

    os.makedirs("reports", exist_ok=True)
    out_json = f"reports/evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def make_json_safe(obj):
        if isinstance(obj, dict):
            return {k: make_json_safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [make_json_safe(v) for v in obj]
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        return obj

    with open(out_json, "w") as f:
        json.dump(make_json_safe(summary), f, indent=4)

    print(f"\nJSON results saved to: {out_json}")


if __name__ == "__main__":
    main()
