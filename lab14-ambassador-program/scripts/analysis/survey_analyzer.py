import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


class SurveyAnalyzer:
    def __init__(self):
        self.data = None
        self.candidates = None

    def load_survey_data(self, file_path):
        """
        Load survey data from CSV or Excel file.

        Supports:
        - .csv
        - .xlsx / .xls

        Validates that required columns exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Survey file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")

        required_cols = [
            "department",
            "years_with_org",
            "security_knowledge",
            "topics_confident",
            "help_frequency",
            "presentation_comfort",
            "ambassador_interest",
            "time_available",
            "motivation_text"
        ]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Normalize numeric fields
        df["security_knowledge"] = pd.to_numeric(df["security_knowledge"], errors="coerce").fillna(1).astype(int)
        df["presentation_comfort"] = pd.to_numeric(df["presentation_comfort"], errors="coerce").fillna(1).astype(int)
        df["ambassador_interest"] = pd.to_numeric(df["ambassador_interest"], errors="coerce").fillna(1).astype(int)

        self.data = df
        return df

    def create_sample_data(self, n_responses=100):
        """
        Generate sample survey data for testing.
        """
        departments = ["IT", "HR", "Finance", "Operations", "Marketing", "Sales", "Other"]
        years_opts = ["<1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
        help_freq_opts = ["Daily", "Weekly", "Monthly", "Rarely", "Never"]
        time_opts = ["1-2 hours", "3-5 hours", "6-10 hours", "10+ hours"]

        topic_pool = [
            "Password security", "Email security", "Social engineering",
            "Data protection", "Mobile security", "Physical security"
        ]

        def random_topics():
            k = np.random.randint(1, 5)
            return "; ".join(np.random.choice(topic_pool, size=k, replace=False))

        def motivation(dept):
            samples = [
                "I want to help colleagues avoid phishing and scams.",
                "Interested in improving our overall security culture.",
                "I enjoy mentoring and would like to support awareness sessions.",
                "Motivated by professional growth and contributing to the organization.",
                "I want to reduce incidents in my department through better practices."
            ]
            return f"[{dept}] {np.random.choice(samples)}"

        rows = []
        for i in range(1, n_responses + 1):
            dept = np.random.choice(departments)
            yrs = np.random.choice(years_opts)

            base = 3
            if dept == "IT":
                base = 4

            sec_know = int(np.clip(np.random.normal(loc=base, scale=1.0), 1, 5))
            amb_interest = int(np.clip(np.random.normal(loc=base, scale=1.2), 1, 5))
            pres_comfort = int(np.clip(np.random.normal(loc=base, scale=1.1), 1, 5))

            help_freq = np.random.choice(help_freq_opts)
            time_avail = np.random.choice(time_opts)

            row = {
                "respondent_id": f"R{i:03d}",
                "department": dept,
                "years_with_org": yrs,
                "security_knowledge": sec_know,
                "topics_confident": random_topics(),
                "help_frequency": help_freq,
                "presentation_comfort": pres_comfort,
                "ambassador_interest": amb_interest,
                "time_available": time_avail,
                "motivation_text": motivation(dept),
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        self.data = df
        return df

    def calculate_ambassador_score(self):
        """
        Calculate ambassador potential score.
        """
        if self.data is None:
            raise ValueError("No data loaded.")

        df = self.data.copy()

        help_map = {"Never": 1, "Rarely": 2, "Monthly": 3, "Weekly": 4, "Daily": 5}
        df["help_score"] = df["help_frequency"].map(help_map).fillna(1).astype(int)

        time_map = {"1-2 hours": 1, "3-5 hours": 2, "6-10 hours": 3, "10+ hours": 4}
        df["time_score"] = df["time_available"].map(time_map).fillna(1).astype(int)
        df["time_score_5"] = (df["time_score"] / 4.0 * 5.0)

        df["ambassador_score"] = (
            0.25 * df["security_knowledge"] +
            0.30 * df["ambassador_interest"] +
            0.20 * df["presentation_comfort"] +
            0.15 * df["help_score"] +
            0.10 * df["time_score_5"]
        ).round(2)

        self.data = df
        return df

    def identify_candidates(self, min_score=3.5):
        if self.data is None or "ambassador_score" not in self.data.columns:
            raise ValueError("Run calculate_ambassador_score() first.")

        candidates = self.data[self.data["ambassador_score"] >= min_score]
        candidates = candidates.sort_values("ambassador_score", ascending=False)

        self.candidates = candidates
        return candidates

    def analyze_by_department(self):
        if self.data is None or "ambassador_score" not in self.data.columns:
            raise ValueError("Run calculate_ambassador_score() first.")

        df = self.data.copy()

        dep = df.groupby("department", as_index=False).agg(
            responses=("respondent_id", "count"),
            avg_security_knowledge=("security_knowledge", "mean"),
            avg_interest=("ambassador_interest", "mean"),
            avg_presentation=("presentation_comfort", "mean"),
            avg_score=("ambassador_score", "mean"),
        ).round(2)

        return dep

    def create_visualizations(self):
        if self.data is None or "ambassador_score" not in self.data.columns:
            raise ValueError("Run calculate_ambassador_score() first.")

        os.makedirs("plots", exist_ok=True)
        df = self.data.copy()

        plt.figure(figsize=(8, 5))
        df["ambassador_interest"].value_counts().sort_index().plot(kind="bar")
        plt.title("Ambassador Interest Distribution")
        plt.tight_layout()
        plt.savefig("plots/interest_distribution.png", dpi=150)
        plt.close()

        plt.figure(figsize=(8, 5))
        df["ambassador_score"].hist(bins=12)
        plt.title("Ambassador Score Distribution")
        plt.tight_layout()
        plt.savefig("plots/score_distribution.png", dpi=150)
        plt.close()

        return [
            "plots/interest_distribution.png",
            "plots/score_distribution.png"
        ]

    def generate_report(self, output_file="analysis_report.txt"):
        if self.data is None or "ambassador_score" not in self.data.columns:
            raise ValueError("Run calculate_ambassador_score() first.")

        total = len(self.data)
        avg_score = self.data["ambassador_score"].mean()

        lines = []
        lines.append("CYBERSECURITY AMBASSADOR PROGRAM - SURVEY ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated at (UTC): {datetime.utcnow().isoformat()}Z")
        lines.append("")
        lines.append(f"Total responses analyzed: {total}")
        lines.append(f"Average ambassador score: {avg_score:.2f}")
        lines.append("")

        if self.candidates is not None:
            lines.append(f"Candidates identified: {len(self.candidates)}")
            lines.append(self.candidates.head(10).to_string(index=False))

        with open(output_file, "w") as f:
            f.write("\n".join(lines))

        return output_file


if __name__ == "__main__":
    analyzer = SurveyAnalyzer()

    df = analyzer.create_sample_data(n_responses=100)
    analyzer.calculate_ambassador_score()
    analyzer.identify_candidates(min_score=3.5)
    analyzer.create_visualizations()
    report_path = analyzer.generate_report()

    print("Analysis complete. Check output files.")
    print("Report:", report_path)
