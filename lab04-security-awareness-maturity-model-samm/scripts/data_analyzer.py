#!/usr/bin/env python3
"""
SAMM Data Analysis Module
Students: Implement statistical analysis and visualization functions
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

plt.switch_backend("Agg")


class SAMMDataAnalyzer:
    def __init__(self):
        self.data = None
        self.analysis_results = {}

    def load_data(self, csv_file):
        """
        Load survey data into pandas DataFrame.

        Args:
            csv_file: Path to CSV file

        Returns:
            Boolean indicating success
        """
        try:
            self.data = pd.read_csv(csv_file)
            print("Loaded survey data successfully.")
            print(f"Rows: {self.data.shape[0]}, Columns: {self.data.shape[1]}")
            print("Columns:", list(self.data.columns))
            print(self.data.head(3).to_string(index=False))
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def _score_columns(self):
        # Identify score columns (exclude metadata)
        meta_cols = {"response_id", "timestamp", "department", "role_level", "years_experience"}
        score_cols = [c for c in self.data.columns if c not in meta_cols]
        return score_cols

    def _category_columns(self):
        # Group score columns into SAMM categories based on prefix
        score_cols = self._score_columns()
        categories = {
            "governance": [c for c in score_cols if c.startswith("governance_")],
            "training": [c for c in score_cols if c.startswith("training_")],
            "culture": [c for c in score_cols if c.startswith("culture_")],
            "measurement": [c for c in score_cols if c.startswith("measurement_")],
        }
        return categories

    def basic_statistics(self):
        """
        Calculate basic statistics for all categories.
        """
        print("\nBasic Statistics Analysis")
        print("=" * 40)

        categories = self._category_columns()
        stats_out = {}

        for cat, cols in categories.items():
            if not cols:
                continue

            # Calculate mean, median, std, min, max for the category (row-wise average then overall)
            cat_series = self.data[cols].mean(axis=1, numeric_only=True)
            cat_stats = {
                "mean": round(float(cat_series.mean()), 3),
                "median": round(float(cat_series.median()), 3),
                "std": round(float(cat_series.std(ddof=1)), 3),
                "min": round(float(cat_series.min()), 3),
                "max": round(float(cat_series.max()), 3),
            }

            stats_out[cat] = cat_stats

            print(f"\nCategory: {cat}")
            for k, v in cat_stats.items():
                print(f"  {k:6}: {v}")

        self.analysis_results["basic_statistics"] = stats_out

    def demographic_analysis(self):
        """
        Analyze scores by demographic factors (department, role).
        """
        print("\nDemographic Analysis")
        print("=" * 40)

        categories = self._category_columns()
        score_cols = self._score_columns()

        # Calculate overall score for each response
        self.data["overall_score"] = self.data[score_cols].mean(axis=1, numeric_only=True)

        dept_summary = {}
        if "department" in self.data.columns:
            dept_group = self.data.groupby("department")["overall_score"]
            dept_summary = dept_group.agg(["count", "mean", "median", "std", "min", "max"]).round(3).to_dict(orient="index")
            print("\nOverall Score by Department:")
            for dept, vals in dept_summary.items():
                print(f"  {dept}: {vals}")

        role_summary = {}
        if "role_level" in self.data.columns:
            role_group = self.data.groupby("role_level")["overall_score"]
            role_summary = role_group.agg(["count", "mean", "median", "std", "min", "max"]).round(3).to_dict(orient="index")
            print("\nOverall Score by Role Level:")
            for role, vals in role_summary.items():
                print(f"  {role}: {vals}")

        self.analysis_results["demographic_analysis"] = {
            "department": dept_summary,
            "role_level": role_summary,
        }

        # Also store category-level demographic averages (optional but useful)
        cat_demo = {"department": {}, "role_level": {}}

        if "department" in self.data.columns:
            for cat, cols in categories.items():
                if cols:
                    self.data[f"{cat}_score"] = self.data[cols].mean(axis=1, numeric_only=True)
                    cat_demo["department"][cat] = self.data.groupby("department")[f"{cat}_score"].mean().round(3).to_dict()

        if "role_level" in self.data.columns:
            for cat, cols in categories.items():
                if cols:
                    self.data[f"{cat}_score"] = self.data[cols].mean(axis=1, numeric_only=True)
                    cat_demo["role_level"][cat] = self.data.groupby("role_level")[f"{cat}_score"].mean().round(3).to_dict()

        self.analysis_results["category_demographics"] = cat_demo

    def correlation_analysis(self):
        """
        Analyze correlations between categories.

        Returns:
            Correlation matrix DataFrame
        """
        print("\nCorrelation Analysis")
        print("=" * 40)

        categories = self._category_columns()
        cat_df = pd.DataFrame()

        for cat, cols in categories.items():
            if cols:
                cat_df[cat] = self.data[cols].mean(axis=1, numeric_only=True)

        if cat_df.empty:
            print("No category columns found for correlation analysis.")
            self.analysis_results["correlation_matrix"] = {}
            return None

        corr = cat_df.corr().round(3)
        print("\nCategory Correlation Matrix:")
        print(corr.to_string())

        self.analysis_results["correlation_matrix"] = corr.to_dict()
        return corr

    def generate_visualizations(self, output_dir):
        """
        Generate visualization plots.

        Args:
            output_dir: Directory to save plots
        """
        os.makedirs(output_dir, exist_ok=True)

        categories = self._category_columns()
        score_cols = self._score_columns()

        # Ensure overall_score exists
        if "overall_score" not in self.data.columns:
            self.data["overall_score"] = self.data[score_cols].mean(axis=1, numeric_only=True)

        # Box plots for category distributions
        cat_scores = {}
        for cat, cols in categories.items():
            if cols:
                cat_scores[cat] = self.data[cols].mean(axis=1, numeric_only=True)

        if cat_scores:
            plt.figure()
            plt.boxplot([cat_scores[c] for c in cat_scores.keys()], labels=list(cat_scores.keys()))
            plt.title("SAMM Category Score Distributions")
            plt.ylabel("Score (1-5)")
            plt.tight_layout()
            box_file = os.path.join(output_dir, "category_boxplots.png")
            plt.savefig(box_file)
            plt.close()

            self.analysis_results["plots"] = self.analysis_results.get("plots", {})
            self.analysis_results["plots"]["category_boxplots"] = box_file

        # Bar charts for demographic comparisons (department)
        if "department" in self.data.columns:
            dept_means = self.data.groupby("department")["overall_score"].mean().sort_values(ascending=False)
            plt.figure()
            plt.bar(dept_means.index.astype(str), dept_means.values)
            plt.title("Average Overall Score by Department")
            plt.ylabel("Average Score (1-5)")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout()
            dept_file = os.path.join(output_dir, "overall_by_department.png")
            plt.savefig(dept_file)
            plt.close()

            self.analysis_results["plots"] = self.analysis_results.get("plots", {})
            self.analysis_results["plots"]["overall_by_department"] = dept_file

        # Bar charts for demographic comparisons (role level)
        if "role_level" in self.data.columns:
            role_means = self.data.groupby("role_level")["overall_score"].mean().sort_values(ascending=False)
            plt.figure()
            plt.bar(role_means.index.astype(str), role_means.values)
            plt.title("Average Overall Score by Role Level")
            plt.ylabel("Average Score (1-5)")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout()
            role_file = os.path.join(output_dir, "overall_by_role_level.png")
            plt.savefig(role_file)
            plt.close()

            self.analysis_results["plots"] = self.analysis_results.get("plots", {})
            self.analysis_results["plots"]["overall_by_role_level"] = role_file

        # Histogram for overall score distribution
        plt.figure()
        plt.hist(self.data["overall_score"].dropna(), bins=10)
        plt.title("Overall Score Distribution")
        plt.xlabel("Overall Score (1-5)")
        plt.ylabel("Count")
        plt.tight_layout()
        hist_file = os.path.join(output_dir, "overall_score_histogram.png")
        plt.savefig(hist_file)
        plt.close()

        self.analysis_results["plots"] = self.analysis_results.get("plots", {})
        self.analysis_results["plots"]["overall_score_histogram"] = hist_file

        print(f"\nPlots saved to: {output_dir}")

    def save_analysis_results(self, output_file):
        """
        Save analysis results to JSON file.

        Args:
            output_file: Path to output JSON file

        Returns:
            Boolean indicating success
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.analysis_results, f, indent=2)
            print(f"Analysis results saved to: {output_file}")
            return True
        except Exception as e:
            print(f"Error saving analysis results: {e}")
            return False

    def run_complete_analysis(self, csv_file, output_dir):
        """
        Run complete data analysis pipeline.

        Args:
            csv_file: Input CSV file path
            output_dir: Output directory for results

        Returns:
            Boolean indicating success
        """
        # Load data
        if not self.load_data(csv_file):
            return False

        # Run all analysis functions
        self.basic_statistics()
        self.demographic_analysis()
        self.correlation_analysis()

        # Generate visualizations
        self.generate_visualizations(output_dir)

        # Save results
        out_json = os.path.join(output_dir, "analysis_results.json")
        return self.save_analysis_results(out_json)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python3 data_analyzer.py <survey_csv_file> <output_dir>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]

    analyzer = SAMMDataAnalyzer()
    ok = analyzer.run_complete_analysis(csv_file, output_dir)

    if not ok:
        sys.exit(1)
