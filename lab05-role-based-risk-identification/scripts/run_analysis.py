#!/usr/bin/env python3
"""
Execute role-based risk analysis
Students: Complete the main analysis workflow
"""

import os
from role_risk_analyzer import RoleRiskAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


def create_risk_visualization(analyzer):
    """
    Create visualizations for risk analysis results.

    Args:
        analyzer: RoleRiskAnalyzer instance with completed analysis
    """
    if not analyzer.risk_scores:
        print("[ERROR] No risk data available")
        return

    # Convert risk_scores to pandas DataFrame
    rows = []
    for role_id, info in analyzer.risk_scores.items():
        rows.append({
            "role_id": role_id,
            "role_name": info["role_name"],
            "department": info["department"],
            "role_type": info["role_type"],
            "base_score": info["base_score"],
            "final_score": info["final_score"],
            "risk_level": info["risk_level"],
        })

    df = pd.DataFrame(rows)

    # Create figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Histogram of risk score distribution
    axes[0, 0].hist(df["final_score"], bins=10)
    axes[0, 0].set_title("Risk Score Distribution")
    axes[0, 0].set_xlabel("Final Risk Score")
    axes[0, 0].set_ylabel("Count")

    # Plot 2: Pie chart of risk level distribution
    lvl_counts = df["risk_level"].value_counts()
    axes[0, 1].pie(lvl_counts.values, labels=lvl_counts.index, autopct="%1.1f%%")
    axes[0, 1].set_title("Risk Level Distribution")

    # Plot 3: Bar chart of average risk by department
    dept_avg = df.groupby("department")["final_score"].mean().sort_values(ascending=False)
    axes[1, 0].bar(dept_avg.index.astype(str), dept_avg.values)
    axes[1, 0].set_title("Average Risk by Department")
    axes[1, 0].set_xlabel("Department")
    axes[1, 0].set_ylabel("Average Final Score")
    axes[1, 0].tick_params(axis="x", rotation=30)

    # Plot 4: Bar chart of average risk by role type
    type_avg = df.groupby("role_type")["final_score"].mean().sort_values(ascending=False)
    axes[1, 1].bar(type_avg.index.astype(str), type_avg.values)
    axes[1, 1].set_title("Average Risk by Role Type")
    axes[1, 1].set_xlabel("Role Type")
    axes[1, 1].set_ylabel("Average Final Score")
    axes[1, 1].tick_params(axis="x", rotation=30)

    plt.tight_layout()

    # Save figure
    out_file = "risk_analysis_charts.png"
    plt.savefig(out_file)
    plt.close()

    print(f"[INFO] Visualization saved: {out_file}")


def generate_detailed_report(analyzer):
    """
    Generate detailed text report.
    """
    if not analyzer.risk_scores:
        print("[ERROR] No risk analysis data available")
        return False

    out_file = "detailed_risk_report.txt"

    sorted_roles = sorted(
        analyzer.risk_scores.items(),
        key=lambda x: x[1]["final_score"],
        reverse=True
    )

    dist = {}
    for _, info in sorted_roles:
        dist[info["risk_level"]] = dist.get(info["risk_level"], 0) + 1

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("DETAILED ROLE RISK REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write("Risk Level Distribution:\n")
        for lvl, count in dist.items():
            f.write(f"- {lvl}: {count}\n")
        f.write("\n")

        f.write("Role-by-Role Analysis (Sorted by Risk Score):\n")
        f.write("-" * 60 + "\n")

        for role_id, info in sorted_roles:
            f.write(f"Role ID: {role_id}\n")
            f.write(f"Role Name: {info['role_name']}\n")
            f.write(f"Department: {info['department']}\n")
            f.write(f"Role Type: {info['role_type']}\n")
            f.write(f"Base Score: {info['base_score']}\n")
            f.write(f"Final Score: {info['final_score']}\n")
            f.write(f"Risk Level: {info['risk_level']}\n")
            f.write(f"Analyzed At: {info['analyzed_at']}\n")
            f.write("-" * 60 + "\n")

    print(f"[INFO] Detailed text report generated: {out_file}")
    return True


def main():
    """Main execution function"""
    print("Starting Role-Based Risk Analysis")
    print("=" * 40)

    analyzer = RoleRiskAnalyzer()

    if not analyzer.load_organizational_data("organizational_roles.json"):
        return

    if not analyzer.load_cti_data("cti_data.json"):
        return

    if not analyzer.analyze_all_roles():
        return

    analyzer.display_top_risks(top_n=10)

    analyzer.generate_risk_report(output_file="comprehensive_risk_report.json")

    generate_detailed_report(analyzer)

    create_risk_visualization(analyzer)

    print("\n[INFO] Analysis completed successfully.")
    print("[INFO] Generated files:")
    print(" - comprehensive_risk_report.json")
    print(" - detailed_risk_report.txt")
    print(" - risk_analysis_charts.png")


if __name__ == "__main__":
    main()
