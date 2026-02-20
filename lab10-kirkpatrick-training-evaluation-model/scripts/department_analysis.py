#!/usr/bin/env python3
"""
Department-specific Kirkpatrick analysis
Department comparison functionality
"""

import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def analyze_by_department(data_file):
    """
    Analyze training effectiveness by department.
    """
    data = pd.read_csv(data_file)

    print("\n=== DEPARTMENT ANALYSIS (LEVELS 1-4) ===")

    departments = sorted(data["department"].unique())
    dept_results = {}

    for dept in departments:
        subset = data[data["department"] == dept]

        reaction_mean = float(subset["reaction_score"].mean())
        pre_avg = float(subset["pre_test"].mean())
        post_avg = float(subset["post_test"].mean())
        improvement_avg = float((subset["post_test"] - subset["pre_test"]).mean())

        incidents_before = float(subset["incidents_before"].sum())
        incidents_after = float(subset["incidents_after"].sum())
        reduction = incidents_before - incidents_after
        reduction_rate = float(reduction / incidents_before) if incidents_before > 0 else 0.0

        impact_avg = float(subset["business_impact"].mean())

        dept_results[dept] = {
            "reaction_mean": reaction_mean,
            "pre_avg": pre_avg,
            "post_avg": post_avg,
            "improvement_avg": improvement_avg,
            "incidents_before_total": incidents_before,
            "incidents_after_total": incidents_after,
            "reduction_rate": reduction_rate,
            "business_impact_avg": impact_avg,
        }

        print(f"\n--- {dept} ---")
        print(f"Level 1 Reaction Mean: {reaction_mean:.2f}")
        print(f"Level 2 Learning Pre Avg: {pre_avg:.2f}, Post Avg: {post_avg:.2f}, Avg Improvement: {improvement_avg:.2f}")
        print(f"Level 3 Behavior Incidents Before: {incidents_before:.0f}, After: {incidents_after:.0f}, Reduction Rate: {reduction_rate:.2f}")
        print(f"Level 4 Results Avg Business Impact: {impact_avg:.2f}")

    def composite_score(d):
        return (
            d["reaction_mean"]
            + d["improvement_avg"] / 10
            + (d["reduction_rate"] * 100) / 10
            + d["business_impact_avg"]
        )

    ranked = sorted(dept_results.items(), key=lambda x: composite_score(x[1]), reverse=True)

    if ranked:
        best = ranked[0]
        worst = ranked[-1]
        print("\n=== DEPARTMENT PERFORMANCE SUMMARY ===")
        print(f"Best Performing Department: {best[0]}")
        print(f"Worst Performing Department: {worst[0]}")

    return dept_results


def compare_departments(data_file):
    """
    Create comparative visualization across departments.
    """
    data = pd.read_csv(data_file)

    os.makedirs("visualizations", exist_ok=True)

    grouped = data.groupby("department").agg(
        reaction_mean=("reaction_score", "mean"),
        incidents_before=("incidents_before", "sum"),
        incidents_after=("incidents_after", "sum"),
        business_impact_mean=("business_impact", "mean"),
    )

    data["improvement"] = data["post_test"] - data["pre_test"]
    improvement_means = data.groupby("department")["improvement"].mean()
    grouped["improvement_mean"] = improvement_means

    grouped["reduction_rate"] = (
        (grouped["incidents_before"] - grouped["incidents_after"])
        / grouped["incidents_before"]
    )
    grouped["reduction_rate"] = grouped["reduction_rate"].replace(
        [float("inf"), -float("inf")], 0
    ).fillna(0)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Department Comparison - Kirkpatrick Metrics", fontsize=16)

    axes[0, 0].bar(grouped.index.astype(str), grouped["reaction_mean"].values, edgecolor="black")
    axes[0, 0].set_title("Avg Reaction Score (Level 1)")
    axes[0, 0].tick_params(axis="x", rotation=30)

    axes[0, 1].bar(grouped.index.astype(str), grouped["improvement_mean"].values, edgecolor="black")
    axes[0, 1].set_title("Avg Learning Improvement (Level 2)")
    axes[0, 1].tick_params(axis="x", rotation=30)

    axes[1, 0].bar(grouped.index.astype(str), grouped["reduction_rate"].values, edgecolor="black")
    axes[1, 0].set_title("Incident Reduction Rate (Level 3)")
    axes[1, 0].tick_params(axis="x", rotation=30)

    axes[1, 1].bar(grouped.index.astype(str), grouped["business_impact_mean"].values, edgecolor="black")
    axes[1, 1].set_title("Avg Business Impact (Level 4)")
    axes[1, 1].tick_params(axis="x", rotation=30)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    out_file = f"visualizations/department_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(out_file)
    plt.close(fig)

    print(f"\nDepartment comparison visualization saved to: {out_file}")
    return out_file


if __name__ == "__main__":
    analyze_by_department("data/training_data.csv")
    compare_departments("data/training_data.csv")
