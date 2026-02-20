#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class VisualizationGenerator:
    def __init__(self, data_file):
        """Initialize with behavior data."""
        self.df = pd.read_csv(data_file)
        self.df["Training_Date"] = pd.to_datetime(self.df["Training_Date"])
        self.df["Knowledge_Improvement"] = self.df["Post_Score"] - self.df["Pre_Score"]

        # Safe style for Ubuntu 24.04
        plt.style.use("seaborn-v0_8")

        self.project_root = Path(__file__).resolve().parent.parent
        self.out_dir = self.project_root / "visualizations"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def create_knowledge_improvement_chart(self):
        """
        Create before/after training comparison chart.
        Saves: knowledge_improvement.png
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        axes[0].hist(self.df["Pre_Score"], bins=10)
        axes[0].set_title("Pre-Training Score Distribution")
        axes[0].set_xlabel("Pre Score")
        axes[0].set_ylabel("Count")

        axes[1].hist(self.df["Post_Score"], bins=10)
        axes[1].set_title("Post-Training Score Distribution")
        axes[1].set_xlabel("Post Score")
        axes[1].set_ylabel("Count")

        fig.suptitle("Knowledge Improvement (Pre vs Post Training)", fontsize=14)
        out_path = self.out_dir / "knowledge_improvement.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return str(out_path)

    def create_behavior_score_dashboard(self):
        """
        Create comprehensive behavior score dashboard.
        Saves: behavior_dashboard.png
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1) Overall score distribution
        axes[0, 0].hist(self.df["Behavior_Score"], bins=12)
        axes[0, 0].set_title("Behavior Score Distribution")
        axes[0, 0].set_xlabel("Behavior Score")
        axes[0, 0].set_ylabel("Count")

        # 2) Scores by department (boxplot)
        sns.boxplot(data=self.df, x="Department", y="Behavior_Score", ax=axes[0, 1])
        axes[0, 1].set_title("Behavior Score by Department")
        axes[0, 1].set_xlabel("Department")
        axes[0, 1].set_ylabel("Behavior Score")
        axes[0, 1].tick_params(axis="x", rotation=30)

        # 3) Risk level pie chart
        risk_counts = self.df["Risk_Level"].value_counts()
        axes[1, 0].pie(risk_counts.values, labels=risk_counts.index, autopct="%1.1f%%")
        axes[1, 0].set_title("Risk Level Distribution")

        # 4) Score vs improvement scatter
        axes[1, 1].scatter(self.df["Knowledge_Improvement"], self.df["Behavior_Score"])
        axes[1, 1].set_title("Behavior Score vs Knowledge Improvement")
        axes[1, 1].set_xlabel("Knowledge Improvement (Post - Pre)")
        axes[1, 1].set_ylabel("Behavior Score")

        fig.suptitle("Behavior Change Dashboard (Static)", fontsize=16)
        out_path = self.out_dir / "behavior_dashboard.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return str(out_path)

    def create_phishing_progression_chart(self):
        """
        Create phishing test progression visualization.
        Saves: phishing_progression.png
        """
        def pass_rate(col):
            return float((self.df[col] == "Passed").mean()) * 100.0

        sim1 = pass_rate("Phishing_Test_1")
        sim2 = pass_rate("Phishing_Test_2")
        sim3 = pass_rate("Phishing_Test_3")

        fig = plt.figure(figsize=(10, 6))
        plt.plot([1, 2, 3], [sim1, sim2, sim3], marker="o")
        plt.xticks([1, 2, 3], ["Sim 1", "Sim 2", "Sim 3"])
        plt.ylim(0, 100)
        plt.title("Phishing Simulation Pass Rate Progression")
        plt.xlabel("Simulation")
        plt.ylabel("Pass Rate (%)")

        # Annotate points
        for x, y in zip([1, 2, 3], [sim1, sim2, sim3]):
            plt.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")

        out_path = self.out_dir / "phishing_progression.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return str(out_path)

    def create_compliance_heatmap(self):
        """
        Create policy compliance heatmap by department.
        Saves: compliance_heatmap.png
        """
        # Convert Yes/No to 1/0
        dfc = self.df.copy()
        dfc["Password_Compliance_Num"] = (dfc["Password_Compliance"] == "Yes").astype(int)
        dfc["MFA_Enabled_Num"] = (dfc["MFA_Enabled"] == "Yes").astype(int)

        agg = dfc.groupby("Department").agg(
            password_compliance=("Password_Compliance_Num", "mean"),
            mfa_enabled=("MFA_Enabled_Num", "mean"),
            avg_incident_reports=("Incident_Reports", "mean"),
        )

        # Convert to percentages for compliance columns
        agg["password_compliance"] = agg["password_compliance"] * 100.0
        agg["mfa_enabled"] = agg["mfa_enabled"] * 100.0

        fig = plt.figure(figsize=(10, 6))
        sns.heatmap(agg, annot=True, fmt=".1f")
        plt.title("Compliance + Reporting Heatmap by Department")
        plt.ylabel("Department")

        out_path = self.out_dir / "compliance_heatmap.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

        return str(out_path)


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "behavior_data.csv"

    generator = VisualizationGenerator(data_file)

    p1 = generator.create_knowledge_improvement_chart()
    print(f"Saved: {p1}")

    p2 = generator.create_behavior_score_dashboard()
    print(f"Saved: {p2}")

    p3 = generator.create_phishing_progression_chart()
    print(f"Saved: {p3}")

    p4 = generator.create_compliance_heatmap()
    print(f"Saved: {p4}")

    print("All visualizations generated successfully.")


if __name__ == "__main__":
    main()
