#!/usr/bin/env python3
"""
Assessment Comparison Tool
"""

import yaml
import matplotlib.pyplot as plt
import os
import sys
from benchmark_analyzer import BenchmarkAnalyzer


def load_multiple_assessments(file_paths: list) -> list:
    """
    Load multiple assessment files for comparison.

    Args:
        file_paths: List of assessment file paths

    Returns:
        List of assessment data dictionaries
    """
    assessments = []

    for p in file_paths:
        with open(p, "r", encoding="utf-8") as f:
            assessments.append(yaml.safe_load(f))

    return assessments


def compare_domain_scores(assessments: list, analyzer: BenchmarkAnalyzer) -> dict:
    """
    Compare domain scores across assessments.

    Args:
        assessments: List of assessment dictionaries
        analyzer: BenchmarkAnalyzer instance

    Returns:
        Dictionary containing comparison results
    """
    comparison = {
        "labels": [],
        "domain_scores": {},  # domain -> list of scores per assessment
        "overall_scores": [],
    }

    # Initialize domain score lists
    for domain in analyzer.domains.keys():
        comparison["domain_scores"][domain] = []

    for a in assessments:
        org = a.get("organization", {})
        label = f"{org.get('name','Org')} ({org.get('date','date')})"
        comparison["labels"].append(label)

        responses = a.get("responses", {})
        domain_scores = {}

        for domain in analyzer.domains.keys():
            domain_scores[domain] = analyzer.calculate_domain_score(
                domain,
                responses.get(domain, [])
            )

        overall = analyzer.calculate_overall_score(domain_scores)
        comparison["overall_scores"].append(overall)

        for domain in analyzer.domains.keys():
            comparison["domain_scores"][domain].append(
                domain_scores[domain]
            )

    return comparison


def generate_trend_chart(comparison_data: dict, output_path: str):
    """
    Generate trend comparison chart.

    Args:
        comparison_data: Comparison results dictionary
        output_path: Path to save chart
    """
    labels = comparison_data["labels"]
    overall = comparison_data["overall_scores"]

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(overall)), overall, marker="o")

    plt.xticks(
        range(len(labels)),
        labels,
        rotation=25,
        ha="right"
    )

    plt.title("Overall Maturity Trend Across Assessments")
    plt.xlabel("Assessment")
    plt.ylabel("Overall Score (%)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 scripts/compare_assessments.py "
            "<assessment1.yaml> <assessment2.yaml> ..."
        )
        sys.exit(1)

    paths = sys.argv[1:]

    analyzer = BenchmarkAnalyzer(
        "config/framework.yaml",
        "data/questions.yaml"
    )

    assessments = load_multiple_assessments(paths)
    comparison_data = compare_domain_scores(assessments, analyzer)

    os.makedirs("reports", exist_ok=True)

    out_chart = "reports/assessment_trend.png"
    generate_trend_chart(comparison_data, out_chart)

    print("[INFO] Comparison complete.")
    print(f"[INFO] Trend chart saved: {out_chart}")
    print("[INFO] Overall scores:", comparison_data["overall_scores"])


if __name__ == "__main__":
    main()
