#!/usr/bin/env python3
"""
Main Benchmarking Execution Script
"""

from benchmark_analyzer import BenchmarkAnalyzer
from report_generator import ReportGenerator
import sys
import os


def main():
    """
    Execute complete benchmarking workflow.
    """
    print("Security Program Benchmarking Tool")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("Usage: python3 scripts/run_benchmark.py <responses_yaml>")
        sys.exit(1)

    responses_path = sys.argv[1]

    config_path = "config/framework.yaml"
    questions_path = "data/questions.yaml"

    # Initialize analyzer with config files
    analyzer = BenchmarkAnalyzer(
        config_path=config_path,
        questions_path=questions_path
    )

    # Load and analyze assessment responses
    results = analyzer.analyze_assessment(responses_path)
    org_info = results.get("organization", {})
    domain_scores = results.get("domain_scores", {})

    # Display results to console
    print("\n[RESULTS]")
    print(f"Organization: {org_info.get('name', 'N/A')}")
    print(f"Overall Score: {results.get('overall_score', 0.0)}%")

    maturity = results.get("maturity_level", {})
    print(f"Maturity Level: {maturity.get('level')} - {maturity.get('name')}")

    print("\nDomain Scores:")
    for d, s in domain_scores.items():
        print(f"- {d}: {s}%")

    # Generate visualizations
    os.makedirs("reports", exist_ok=True)

    report_gen = ReportGenerator(results=results, org_info=org_info)
    report_gen.generate_bar_chart(
        domain_scores,
        "reports/domain_scores.png"
    )

    # Generate markdown report
    report_gen.generate_markdown_report(
        "reports/assessment_report.md"
    )

    print("\n[INFO] Outputs generated:")
    print(" - reports/domain_scores.png")
    print(" - reports/assessment_report.md")


if __name__ == "__main__":
    main()
