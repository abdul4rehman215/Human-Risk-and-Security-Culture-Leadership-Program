#!/usr/bin/env python3
"""
Custom analysis queries for training evaluation
"""

import pandas as pd


def find_top_performers(data_file, n=5):
    """
    Identify top performing participants across all metrics.
    """
    data = pd.read_csv(data_file)

    # Calculate improvement
    data["improvement"] = data["post_test"] - data["pre_test"]

    # Calculate behavior improvement rate
    def behavior_rate(row):
        b = row["incidents_before"]
        a = row["incidents_after"]
        if b <= 0:
            return 0.0
        return (b - a) / b

    data["behavior_rate"] = data.apply(behavior_rate, axis=1)

    # Composite score calculation
    # Reaction (1–5) scaled to 0–100 by *20
    # Improvement scaled by *2
    # Behavior rate scaled to 0–100
    # Business impact (1–10) scaled to 0–100 by *10
    data["composite_score"] = (
        (data["reaction_score"] * 20.0)
        + (data["improvement"] * 2.0)
        + (data["behavior_rate"] * 100.0)
        + (data["business_impact"] * 10.0)
    )

    top = data.sort_values("composite_score", ascending=False).head(n)

    print(f"\n=== TOP {n} PERFORMERS ===")
    for _, row in top.iterrows():
        print(
            f"Participant {row['participant_id']} ({row['department']}): "
            f"Composite={row['composite_score']:.2f}, "
            f"Reaction={row['reaction_score']}, "
            f"Improvement={row['improvement']}, "
            f"BehaviorRate={row['behavior_rate']:.2f}, "
            f"BusinessImpact={row['business_impact']}"
        )

    return top


def identify_improvement_areas(data_file):
    """
    Identify areas needing improvement based on defined thresholds.
    """
    data = pd.read_csv(data_file)

    print("\n=== IMPROVEMENT AREAS ===")

    # Level 1 – Reaction
    reaction_mean = data["reaction_score"].mean()
    if reaction_mean < 4.0:
        print("- Level 1 Reaction: Average reaction below 4.0, improve engagement and delivery.")

    # Level 2 – Learning
    improvement_mean = (data["post_test"] - data["pre_test"]).mean()
    if improvement_mean < 15:
        print("- Level 2 Learning: Average improvement below 15 points, add reinforcement and practice.")

    passing_rate = (data["post_test"] >= 80).mean() * 100
    if passing_rate < 80:
        print("- Level 2 Learning: Passing rate below 80%, improve clarity and offer remediation.")

    # Level 3 – Behavior
    total_before = data["incidents_before"].sum()
    total_after = data["incidents_after"].sum()
    reduction_rate = (total_before - total_after) / total_before if total_before > 0 else 0

    if reduction_rate < 0.5:
        print("- Level 3 Behavior: Incident reduction below 50%, increase follow-ups and simulations.")

    # Level 4 – Results
    impact_mean = data["business_impact"].mean()
    if impact_mean < 8.0:
        print("- Level 4 Results: Business impact below 8.0, align training to business objectives.")

    # If everything meets targets
    if (
        reaction_mean >= 4.0
        and improvement_mean >= 15
        and passing_rate >= 80
        and reduction_rate >= 0.5
        and impact_mean >= 8.0
    ):
        print("- No major improvement areas detected; continue monitoring and optimize gradually.")


if __name__ == "__main__":
    find_top_performers("data/training_data.csv")
    identify_improvement_areas("data/training_data.csv")
