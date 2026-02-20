#!/usr/bin/env python3
"""
Impact Metrics Analyzer
"""
import pandas as pd
import numpy as np


class ImpactAnalyzer:
    def __init__(self, data_file="impact_metrics.csv"):
        self.data_file = data_file
        self.df = pd.read_csv(self.data_file)
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m", errors="coerce")

        num_cols = [
            "voluntary_incident_reports",
            "security_discussions_initiated",
            "proactive_security_behaviors",
            "peer_coaching_instances",
            "security_incidents",
            "culture_maturity_score",
        ]
        for c in num_cols:
            self.df[c] = pd.to_numeric(self.df[c], errors="coerce")

        self.df = self.df.dropna(subset=["date", "department"])

    def behavioral_change_analysis(self):
        df = self.df.sort_values(["department", "date"])
        metrics = [
            "voluntary_incident_reports",
            "security_discussions_initiated",
            "proactive_security_behaviors",
            "peer_coaching_instances",
        ]

        print("\n" + "=" * 70)
        print("IMPACT: BEHAVIORAL CHANGE ANALYSIS (First vs Last Month)")
        print("=" * 70)

        results = []
        for dept, sub in df.groupby("department"):
            first = sub.iloc[0]
            last = sub.iloc[-1]
            row = {"department": dept}
            for m in metrics:
                start = float(first[m])
                end = float(last[m])
                pct = ((end - start) / start * 100.0) if start != 0 else 0.0
                row[f"{m}_start"] = start
                row[f"{m}_end"] = end
                row[f"{m}_pct_change"] = pct
            results.append(row)

        res_df = pd.DataFrame(results)

        for _, r in res_df.iterrows():
            print(f"\nDepartment: {r['department']}")
            for m in metrics:
                print(f"  {m}: {int(r[f'{m}_start'])} -> {int(r[f'{m}_end'])}  ({r[f'{m}_pct_change']:.1f}%)")

        return res_df

    def culture_maturity_assessment(self):
        def level(score):
            if score <= 40:
                return "Basic"
            if score <= 60:
                return "Developing"
            if score <= 80:
                return "Defined"
            if score <= 90:
                return "Managed"
            return "Optimized"

        dept = (
            self.df.groupby("department", as_index=False)["culture_maturity_score"]
            .mean()
            .sort_values("culture_maturity_score", ascending=False)
        )
        dept["maturity_level"] = dept["culture_maturity_score"].apply(level)

        avg_maturity = float(self.df["culture_maturity_score"].mean())

        print("\n" + "=" * 70)
        print("IMPACT: CULTURE MATURITY ASSESSMENT")
        print("=" * 70)
        print(f"Overall Average Maturity Score: {avg_maturity:.2f}")

        for _, r in dept.iterrows():
            print(f"{r['department']:<12} {r['culture_maturity_score']:.2f}  ->  {r['maturity_level']}")

        return dept

    def proactive_behavior_analysis(self):
        df = self.df.copy()
        df["total_proactive"] = (
            df["voluntary_incident_reports"]
            + df["security_discussions_initiated"]
            + df["proactive_security_behaviors"]
            + df["peer_coaching_instances"]
        )

        dept = (
            df.groupby("department", as_index=False)
            .agg(avg_proactive=("total_proactive", "mean"),
                 avg_incidents=("security_incidents", "mean"))
            .sort_values("avg_proactive", ascending=False)
        )

        print("\n" + "=" * 70)
        print("IMPACT: PROACTIVE BEHAVIOR ANALYSIS")
        print("=" * 70)

        for _, r in dept.iterrows():
            print(f"{r['department']:<12} proactive_avg={r['avg_proactive']:.2f}  incidents_avg={r['avg_incidents']:.2f}")

        return dept

    def incident_reduction_analysis(self):
        df = self.df.copy().sort_values("date")
        monthly = df.groupby("date", as_index=False).agg(
            incidents=("security_incidents", "sum"),
            maturity=("culture_maturity_score", "mean"),
        )

        start_inc = float(monthly["incidents"].iloc[0])
        end_inc = float(monthly["incidents"].iloc[-1])
        reduction_pct = ((start_inc - end_inc) / start_inc * 100.0) if start_inc != 0 else 0.0

        corr = monthly[["incidents", "maturity"]].corr().iloc[0, 1]

        print("\n" + "=" * 70)
        print("IMPACT: INCIDENT REDUCTION ANALYSIS")
        print("=" * 70)
        print(f"Incidents (start -> end): {int(start_inc)} -> {int(end_inc)}")
        print(f"Reduction Percentage: {reduction_pct:.2f}%")
        print(f"Correlation (Incidents vs Maturity): {corr:.3f}")

        roi_indicator = "Strong" if reduction_pct >= 20 else "Moderate" if reduction_pct >= 10 else "Weak"
        print(f"ROI Indicator: {roi_indicator}")

        return monthly, reduction_pct, float(corr), roi_indicator

    def generate_impact_report(self):
        self.behavioral_change_analysis()
        maturity_df = self.culture_maturity_assessment()
        proactive_df = self.proactive_behavior_analysis()
        monthly_df, reduction_pct, corr, roi_indicator = self.incident_reduction_analysis()

        with open("impact_report.txt", "w") as f:
            f.write("IMPACT METRICS REPORT\n\n")
            f.write(maturity_df.to_string(index=False))
            f.write("\n\n")
            f.write(proactive_df.to_string(index=False))
            f.write("\n\nIncident Reduction: {:.2f}%\n".format(reduction_pct))
            f.write("ROI Indicator: {}\n".format(roi_indicator))

        print("\nSaved: impact_report.txt")


if __name__ == "__main__":
    analyzer = ImpactAnalyzer()
    analyzer.generate_impact_report()
