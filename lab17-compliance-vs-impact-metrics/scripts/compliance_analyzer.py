#!/usr/bin/env python3
"""
Compliance Metrics Analyzer
"""
import pandas as pd
import numpy as np


class ComplianceAnalyzer:
    def __init__(self, data_file="compliance_metrics.csv"):
        self.data_file = data_file
        self.df = pd.read_csv(self.data_file)
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m", errors="coerce")

        num_cols = [
            "training_completion_rate",
            "policy_acknowledgment_rate",
            "phishing_click_rate",
            "assessment_pass_rate",
            "compliance_score",
            "department_size",
        ]
        for c in num_cols:
            self.df[c] = pd.to_numeric(self.df[c], errors="coerce")

        self.df = self.df.dropna(subset=["date", "department"])

    def calculate_statistics(self):
        metrics = [
            "training_completion_rate",
            "policy_acknowledgment_rate",
            "phishing_click_rate",
            "assessment_pass_rate",
            "compliance_score",
        ]
        summary = []
        for m in metrics:
            series = self.df[m].dropna()
            summary.append(
                {
                    "metric": m,
                    "mean": float(series.mean()),
                    "median": float(series.median()),
                    "std": float(series.std(ddof=1)) if len(series) > 1 else 0.0,
                    "min": float(series.min()),
                    "max": float(series.max()),
                }
            )
        return pd.DataFrame(summary)

    def department_comparison(self):
        dept = (
            self.df.groupby("department", as_index=False)["compliance_score"]
            .mean()
            .sort_values("compliance_score", ascending=False)
        )

        best = dept.iloc[0]
        worst = dept.iloc[-1]

        print("\n" + "=" * 70)
        print("COMPLIANCE: DEPARTMENT COMPARISON (Avg Compliance Score %)")
        print("=" * 70)
        for _, row in dept.iterrows():
            print(f"{row['department']:<12}  {row['compliance_score']:.2f}%")

        print("\nBest Performer:")
        print(f"  {best['department']} ({best['compliance_score']:.2f}%)")
        print("Worst Performer:")
        print(f"  {worst['department']} ({worst['compliance_score']:.2f}%)")

        return dept

    def trend_analysis(self):
        monthly = self.df.groupby("date", as_index=False).mean(numeric_only=True)

        x = np.arange(len(monthly))
        y = monthly["compliance_score"].values

        slope = np.polyfit(x, y, 1)[0] if len(x) >= 2 else 0.0
        direction = "improving" if slope > 0.05 else ("declining" if slope < -0.05 else "stable")

        print("\n" + "=" * 70)
        print("COMPLIANCE: TREND ANALYSIS")
        print("=" * 70)
        print(f"Trend direction (compliance_score): {direction}")
        print(f"Rate of change (approx slope): {slope:.4f} score points/month")

        return monthly, direction, float(slope)

    def identify_gaps(self):
        thresholds = {
            "training_completion_rate": 90.0,
            "policy_acknowledgment_rate": 90.0,
            "assessment_pass_rate": 85.0,
            "phishing_click_rate": 10.0,
            "compliance_score": 85.0,
        }

        df = self.df.copy()
        gaps = []

        for metric, threshold in thresholds.items():
            if metric == "phishing_click_rate":
                gap = df[df[metric] > threshold].copy()
                gap["gap_amount"] = gap[metric] - threshold
            else:
                gap = df[df[metric] < threshold].copy()
                gap["gap_amount"] = threshold - gap[metric]

            gap["gap_metric"] = metric
            gap["threshold"] = threshold
            gaps.append(gap)

        gap_df = pd.concat(gaps, ignore_index=True) if gaps else pd.DataFrame()

        print("\n" + "=" * 70)
        print("COMPLIANCE: GAP IDENTIFICATION")
        print("=" * 70)

        if gap_df.empty:
            print("No gaps found.")
            return gap_df

        summary = (
            gap_df.groupby(["department", "gap_metric"], as_index=False)
            .agg(count=("gap_amount", "count"), avg_gap=("gap_amount", "mean"))
            .sort_values(["count", "avg_gap"], ascending=False)
        )

        for _, r in summary.iterrows():
            print(f"- {r['department']:<12} {r['gap_metric']:<26} count={int(r['count'])} avg_gap={r['avg_gap']:.2f}")

        return gap_df

    def generate_report(self):
        stats_df = self.calculate_statistics()
        dept_df = self.department_comparison()
        monthly_df, direction, slope = self.trend_analysis()
        gaps_df = self.identify_gaps()

        print("\n" + "=" * 70)
        print("COMPLIANCE: EXECUTIVE SUMMARY")
        print("=" * 70)

        avg_score = float(self.df["compliance_score"].mean())
        avg_phish = float(self.df["phishing_click_rate"].mean())
        avg_train = float(self.df["training_completion_rate"].mean())

        print(f"Average Compliance Score: {avg_score:.2f}%")
        print(f"Average Training Completion Rate: {avg_train:.2f}%")
        print(f"Average Phishing Click Rate: {avg_phish:.2f}%")
        print(f"Trend: {direction} (slope {slope:.4f})")

        recs = []
        if avg_train < 90:
            recs.append("- Increase completion through manager follow-ups.")
        if avg_phish > 10:
            recs.append("- Increase phishing simulations + micro-lessons.")
        if avg_score < 85:
            recs.append("- Use targeted interventions by department.")
        if not recs:
            recs.append("- Maintain current compliance program.")

        print("\nActionable Recommendations:")
        for r in recs:
            print(r)

        with open("compliance_report.txt", "w") as f:
            f.write("COMPLIANCE METRICS REPORT\n\n")
            f.write(stats_df.to_string(index=False))
            f.write("\n\n")
            f.write(dept_df.to_string(index=False))
            f.write("\n\nTREND\n")
            f.write(f"{direction} slope={slope:.4f}\n")
            f.write("\nRECOMMENDATIONS\n")
            f.write("\n".join([r.replace("- ", "") for r in recs]))

        print("\nSaved: compliance_report.txt")


if __name__ == "__main__":
    analyzer = ComplianceAnalyzer()
    analyzer.generate_report()
