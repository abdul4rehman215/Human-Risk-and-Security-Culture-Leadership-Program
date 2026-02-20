import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime


class MetricsDashboard:
    def __init__(self):
        self.metrics_data = {}
        self.kpis = {}

    def load_metrics(self, file_path):
        """
        Load metrics data from file.

        Supports:
        - JSON (recommended: exports/metrics.json from program_tracker.py)
        - CSV (must contain known columns; script will aggregate)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Metrics file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Metrics JSON must be an object/dictionary.")
            self.metrics_data = data

        elif ext == ".csv":
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError("CSV is empty.")

            cols = set(df.columns)
            if {"ambassador_id", "activity_type", "participants", "date"}.issubset(cols):
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["participants"] = pd.to_numeric(df["participants"], errors="coerce").fillna(0).astype(int)
                df["month"] = df["date"].dt.to_period("M").astype(str)

                monthly = df.groupby("month").agg(
                    activities=("activity_type", "count"),
                    participants=("participants", "sum")
                ).reset_index()

                self.metrics_data = {
                    "total_ambassadors": int(df["ambassador_id"].nunique()),
                    "total_activities": int(len(df)),
                    "total_people_reached": int(df["participants"].sum()),
                    "department_coverage": {},
                    "activities_per_ambassador_avg": round(float(df.groupby("ambassador_id").size().mean()), 2),
                    "monthly_trends": monthly.to_dict(orient="records")
                }
            else:
                raise ValueError("CSV format not recognized. Provide activities CSV or a JSON metrics file.")

        else:
            raise ValueError("Unsupported file type. Use .json or .csv")

        for key in ["total_ambassadors", "total_activities", "total_people_reached"]:
            if key not in self.metrics_data:
                raise ValueError(f"Missing required metric key: {key}")

        return self.metrics_data

    def calculate_kpis(self):
        """
        Calculate KPIs (proxies for participation/reach/impact).
        """
        m = self.metrics_data

        total_ambassadors = int(m.get("total_ambassadors", 0))
        total_activities = int(m.get("total_activities", 0))
        total_people = int(m.get("total_people_reached", 0))

        active_ambassadors = total_ambassadors
        if total_ambassadors > 0 and isinstance(m.get("activities_per_ambassador_avg", None), (int, float)):
            if float(m["activities_per_ambassador_avg"]) == 0:
                active_ambassadors = 0

        participation_rate = (active_ambassadors / total_ambassadors * 100.0) if total_ambassadors else 0.0

        reach_per_activity = (total_people / total_activities) if total_activities else 0.0
        reach_per_ambassador = (total_people / total_ambassadors) if total_ambassadors else 0.0

        monthly = m.get("monthly_trends", [])
        trend = {"latest_month": None, "prev_month": None, "activity_change_pct": 0.0, "reach_change_pct": 0.0}

        if isinstance(monthly, list) and len(monthly) >= 2:
            monthly_sorted = sorted(monthly, key=lambda x: x.get("month", ""))
            last = monthly_sorted[-1]
            prev = monthly_sorted[-2]

            last_act = float(last.get("activities", 0))
            prev_act = float(prev.get("activities", 0))
            last_reach = float(last.get("participants", 0))
            prev_reach = float(prev.get("participants", 0))

            act_change = ((last_act - prev_act) / prev_act * 100.0) if prev_act else (100.0 if last_act > 0 else 0.0)
            reach_change = ((last_reach - prev_reach) / prev_reach * 100.0) if prev_reach else (100.0 if last_reach > 0 else 0.0)

            trend = {
                "latest_month": last.get("month"),
                "prev_month": prev.get("month"),
                "activity_change_pct": round(act_change, 2),
                "reach_change_pct": round(reach_change, 2),
            }

        act_norm = min(total_activities / 50.0, 1.0)
        reach_norm = min(total_people / 1000.0, 1.0)
        growth_norm = min(max((trend["activity_change_pct"] + trend["reach_change_pct"]) / 200.0, 0.0), 1.0)

        impact_score = (0.4 * act_norm + 0.4 * reach_norm + 0.2 * growth_norm) * 100.0

        self.kpis = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "participation_rate_pct": round(participation_rate, 2),
            "reach_per_activity": round(reach_per_activity, 2),
            "reach_per_ambassador": round(reach_per_ambassador, 2),
            "impact_score_0_100": round(impact_score, 2),
            "trend": trend
        }

        return self.kpis

    def create_dashboard(self):
        """
        Generate a 6-panel dashboard image.
        """
        os.makedirs("metrics_charts", exist_ok=True)

        m = self.metrics_data
        k = self.kpis if self.kpis else self.calculate_kpis()

        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle("Ambassador Program Metrics Dashboard", fontsize=16)

        # Panel 1: Totals
        axes[0, 0].axis("off")
        totals_text = (
            f"Total Ambassadors: {m.get('total_ambassadors', 0)}\n"
            f"Total Activities: {m.get('total_activities', 0)}\n"
            f"Total People Reached: {m.get('total_people_reached', 0)}\n"
        )
        axes[0, 0].text(0.02, 0.85, "Program Totals", fontsize=14, fontweight="bold")
        axes[0, 0].text(0.02, 0.65, totals_text, fontsize=12)

        # Panel 2: Monthly activities
        monthly = m.get("monthly_trends", [])
        if isinstance(monthly, list) and len(monthly) > 0:
            months = [r.get("month") for r in monthly]
            acts = [r.get("activities", 0) for r in monthly]
            axes[0, 1].plot(months, acts, marker="o")
            axes[0, 1].set_title("Monthly Activity Trend")
            axes[0, 1].set_xlabel("Month")
            axes[0, 1].set_ylabel("Activities")
            axes[0, 1].tick_params(axis="x", rotation=30)
        else:
            axes[0, 1].text(0.5, 0.5, "No monthly trend data", ha="center", va="center")
            axes[0, 1].set_title("Monthly Activity Trend")

        # Panel 3: Monthly reach
        if isinstance(monthly, list) and len(monthly) > 0:
            months = [r.get("month") for r in monthly]
            reach = [r.get("participants", 0) for r in monthly]
            axes[1, 0].plot(months, reach, marker="o")
            axes[1, 0].set_title("Monthly Reach Trend")
            axes[1, 0].set_xlabel("Month")
            axes[1, 0].set_ylabel("People Reached")
            axes[1, 0].tick_params(axis="x", rotation=30)
        else:
            axes[1, 0].text(0.5, 0.5, "No reach trend data", ha="center", va="center")
            axes[1, 0].set_title("Monthly Reach Trend")

        # Panel 4: Department coverage
        dept_cov = m.get("department_coverage", {})
        if isinstance(dept_cov, dict) and len(dept_cov) > 0:
            labels = list(dept_cov.keys())
            values = list(dept_cov.values())
            axes[1, 1].pie(values, labels=labels, autopct="%1.1f%%")
            axes[1, 1].set_title("Ambassador Department Coverage")
        else:
            axes[1, 1].text(0.5, 0.5, "No department coverage data", ha="center", va="center")
            axes[1, 1].set_title("Ambassador Department Coverage")

        # Panel 5: Reach per ambassador
        axes[2, 0].bar(["Reach/Ambassador"], [k.get("reach_per_ambassador", 0)])
        axes[2, 0].set_title("Average Reach per Ambassador")
        axes[2, 0].set_ylabel("People")

        # Panel 6: KPI box
        axes[2, 1].axis("off")
        trend = k.get("trend", {})
        kpi_text = (
            f"Participation Rate: {k.get('participation_rate_pct', 0)}%\n"
            f"Reach per Activity: {k.get('reach_per_activity', 0)}\n"
            f"Impact Score (0-100): {k.get('impact_score_0_100', 0)}\n\n"
            f"Latest Month: {trend.get('latest_month')}\n"
            f"Prev Month: {trend.get('prev_month')}\n"
            f"Activity Change: {trend.get('activity_change_pct', 0)}%\n"
            f"Reach Change: {trend.get('reach_change_pct', 0)}%\n"
        )
        axes[2, 1].text(0.02, 0.90, "KPI Summary", fontsize=14, fontweight="bold")
        axes[2, 1].text(0.02, 0.70, kpi_text, fontsize=12)

        out_path = "metrics_charts/metrics_dashboard.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return out_path

    def generate_executive_summary(self):
        """
        Build executive summary text (string).
        """
        m = self.metrics_data
        k = self.kpis if self.kpis else self.calculate_kpis()

        trend = k.get("trend", {})
        lines = []
        lines.append("AMBASSADOR PROGRAM - EXECUTIVE SUMMARY")
        lines.append("=" * 60)
        lines.append(f"Generated at (UTC): {datetime.utcnow().isoformat()}Z")
        lines.append("")
        lines.append("KEY TOTALS")
        lines.append("-" * 60)
        lines.append(f"Total Ambassadors: {m.get('total_ambassadors', 0)}")
        lines.append(f"Total Activities: {m.get('total_activities', 0)}")
        lines.append(f"Total People Reached: {m.get('total_people_reached', 0)}")
        lines.append("")
        lines.append("KPI SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Participation Rate: {k.get('participation_rate_pct', 0)}%")
        lines.append(f"Reach per Activity: {k.get('reach_per_activity', 0)}")
        lines.append(f"Reach per Ambassador: {k.get('reach_per_ambassador', 0)}")
        lines.append(f"Impact Score (0-100): {k.get('impact_score_0_100', 0)}")
        lines.append("")
        lines.append("TRENDS")
        lines.append("-" * 60)
        lines.append(f"Latest Month: {trend.get('latest_month')}")
        lines.append(f"Previous Month: {trend.get('prev_month')}")
        lines.append(f"Activity Change: {trend.get('activity_change_pct', 0)}%")
        lines.append(f"Reach Change: {trend.get('reach_change_pct', 0)}%")
        lines.append("")
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 60)

        recs = []
        if k.get("participation_rate_pct", 0) < 70:
            recs.append("Increase ambassador engagement: add recognition, simplify monthly expectations, and provide more support materials.")
        if k.get("reach_per_activity", 0) < 15:
            recs.append("Boost attendance: schedule sessions at better times, coordinate with managers, and offer short (15-min) micro-sessions.")
        if trend.get("activity_change_pct", 0) < 0:
            recs.append("Address declining activity: run a quarterly planning meeting and publish a campaign calendar.")
        if k.get("impact_score_0_100", 0) < 40:
            recs.append("Scale program reach: recruit additional ambassadors in underrepresented departments and expand the activity mix.")
        if not recs:
            recs.append("Program performance is healthy. Continue current cadence and focus on consistent reporting and quarterly improvements.")

        for i, r in enumerate(recs, 1):
            lines.append(f"{i}. {r}")

        return "\n".join(lines)


if __name__ == "__main__":
    dashboard = MetricsDashboard()

    metrics_path_json = "exports/metrics.json"
    metrics_path_csv = "exports/activities.csv"

    if os.path.exists(metrics_path_json):
        dashboard.load_metrics(metrics_path_json)
    elif os.path.exists(metrics_path_csv):
        dashboard.load_metrics(metrics_path_csv)
    else:
        raise FileNotFoundError("No metrics found. Run program_tracker.py first to generate exports/.")

    dashboard.calculate_kpis()
    chart_path = dashboard.create_dashboard()
    summary_text = dashboard.generate_executive_summary()

    os.makedirs("exports", exist_ok=True)
    summary_file = "exports/executive_summary.txt"
    with open(summary_file, "w") as f:
        f.write(summary_text)

    print("Dashboard generated:", chart_path)
    print("Executive summary saved:", summary_file)
