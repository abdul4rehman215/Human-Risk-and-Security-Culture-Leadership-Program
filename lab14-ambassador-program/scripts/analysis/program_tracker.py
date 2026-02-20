import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt


class AmbassadorProgramTracker:
    def __init__(self):
        self.ambassadors = []
        self.activities = []
        self.metrics = {}

    def add_ambassador(self, name, department, start_date):
        """
        Add new ambassador to tracking system.
        """
        ambassador_id = f"AMB{len(self.ambassadors) + 1:03d}"

        record = {
            "ambassador_id": ambassador_id,
            "name": name,
            "department": department,
            "start_date": start_date,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "total_activities": 0,
            "total_people_reached": 0,
            "last_activity_date": None
        }

        self.ambassadors.append(record)
        return record

    def log_activity(self, ambassador_id, activity_type, participants, date=None):
        """
        Log ambassador activity and update metrics.
        """
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")

        activity_id = f"ACT{len(self.activities) + 1:04d}"

        activity = {
            "activity_id": activity_id,
            "ambassador_id": ambassador_id,
            "activity_type": activity_type,
            "participants": int(participants),
            "date": date,
            "logged_at": datetime.utcnow().isoformat() + "Z",
        }

        self.activities.append(activity)

        # Update ambassador metrics
        for amb in self.ambassadors:
            if amb["ambassador_id"] == ambassador_id:
                amb["total_activities"] += 1
                amb["total_people_reached"] += int(participants)
                amb["last_activity_date"] = date
                break

        return activity

    def calculate_metrics(self):
        """
        Calculate overall program metrics.
        """
        amb_df = pd.DataFrame(self.ambassadors) if self.ambassadors else pd.DataFrame()
        act_df = pd.DataFrame(self.activities) if self.activities else pd.DataFrame()

        metrics = {}

        metrics["total_ambassadors"] = int(len(self.ambassadors))
        metrics["total_activities"] = int(len(self.activities))
        metrics["total_people_reached"] = int(act_df["participants"].sum()) if not act_df.empty else 0

        if not act_df.empty and not amb_df.empty:
            acts_per_amb = act_df.groupby("ambassador_id").size().reset_index(name="activities")
            metrics["activities_per_ambassador_avg"] = round(float(acts_per_amb["activities"].mean()), 2)

            dept_cov = amb_df["department"].value_counts().to_dict()
            metrics["department_coverage"] = {k: int(v) for k, v in dept_cov.items()}

            act_df["date"] = pd.to_datetime(act_df["date"])
            act_df["month"] = act_df["date"].dt.to_period("M").astype(str)
            monthly = act_df.groupby("month").agg(
                activities=("activity_id", "count"),
                participants=("participants", "sum")
            ).reset_index()

            metrics["monthly_trends"] = monthly.to_dict(orient="records")
        else:
            metrics["activities_per_ambassador_avg"] = 0.0
            metrics["department_coverage"] = {}
            metrics["monthly_trends"] = []

        self.metrics = metrics
        return metrics

    def generate_dashboard(self):
        """
        Create visual dashboard.
        """
        os.makedirs("tracking_charts", exist_ok=True)

        amb_df = pd.DataFrame(self.ambassadors) if self.ambassadors else pd.DataFrame()
        act_df = pd.DataFrame(self.activities) if self.activities else pd.DataFrame()

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Activities per ambassador
        if not act_df.empty:
            counts = act_df["ambassador_id"].value_counts()
            axes[0, 0].bar(counts.index, counts.values)
            axes[0, 0].set_title("Activities by Ambassador")
        else:
            axes[0, 0].text(0.5, 0.5, "No activities logged", ha="center")

        # People reached
        if not amb_df.empty:
            axes[0, 1].bar(amb_df["ambassador_id"], amb_df["total_people_reached"])
            axes[0, 1].set_title("People Reached by Ambassador")
        else:
            axes[0, 1].text(0.5, 0.5, "No ambassadors added", ha="center")

        # Department coverage
        if not amb_df.empty:
            dept_counts = amb_df["department"].value_counts()
            axes[1, 0].pie(dept_counts.values, labels=dept_counts.index, autopct="%1.1f%%")
            axes[1, 0].set_title("Department Coverage")
        else:
            axes[1, 0].text(0.5, 0.5, "No data", ha="center")

        # Monthly trend
        if not act_df.empty:
            act_df["date"] = pd.to_datetime(act_df["date"])
            act_df["month"] = act_df["date"].dt.to_period("M").astype(str)
            monthly = act_df.groupby("month").size()
            axes[1, 1].plot(monthly.index, monthly.values, marker="o")
            axes[1, 1].set_title("Monthly Activity Trend")
        else:
            axes[1, 1].text(0.5, 0.5, "No monthly data", ha="center")

        fig.suptitle("Ambassador Program Dashboard")
        out_path = "tracking_charts/program_dashboard.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return out_path

    def export_data(self):
        """
        Export CSV and JSON metrics.
        """
        os.makedirs("exports", exist_ok=True)

        amb_df = pd.DataFrame(self.ambassadors)
        act_df = pd.DataFrame(self.activities)

        amb_csv = "exports/ambassadors.csv"
        act_csv = "exports/activities.csv"
        met_json = "exports/metrics.json"

        amb_df.to_csv(amb_csv, index=False)
        act_df.to_csv(act_csv, index=False)

        self.calculate_metrics()
        with open(met_json, "w") as f:
            json.dump(self.metrics, f, indent=2)

        return {
            "ambassadors_csv": amb_csv,
            "activities_csv": act_csv,
            "metrics_json": met_json
        }


if __name__ == "__main__":
    tracker = AmbassadorProgramTracker()

    tracker.add_ambassador("Ayesha Khan", "IT", "2026-01-01")
    tracker.add_ambassador("Rohan Mehta", "Finance", "2026-01-01")
    tracker.add_ambassador("Sara Ali", "HR", "2026-01-01")
    tracker.add_ambassador("Hamza Siddiqui", "Operations", "2026-01-01")

    tracker.log_activity("AMB001", "Awareness Session", 25, "2026-01-10")
    tracker.log_activity("AMB001", "Phishing Briefing", 18, "2026-01-24")
    tracker.log_activity("AMB002", "Invoice Fraud Workshop", 20, "2026-01-15")
    tracker.log_activity("AMB003", "New Hire Orientation", 30, "2026-01-20")
    tracker.log_activity("AMB004", "Password Hygiene Session", 22, "2026-01-28")

    tracker.calculate_metrics()
    dashboard_path = tracker.generate_dashboard()
    exports = tracker.export_data()

    print("Program tracking complete.")
    print("Dashboard:", dashboard_path)
    print("Exports:", exports)
