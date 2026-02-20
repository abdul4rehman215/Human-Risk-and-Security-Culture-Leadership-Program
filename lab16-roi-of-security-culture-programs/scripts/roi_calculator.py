import pandas as pd
import numpy as np
import json
from pathlib import Path


class SecurityCultureROICalculator:
    """
    Calculate ROI metrics for security culture programs.
    """

    def __init__(self, data_file):
        """
        Initialize calculator with data file.

        Args:
            data_file: Path to CSV file with security metrics
        """
        # Load data from CSV
        self.data_file = Path(data_file)
        if not self.data_file.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_file}")

        self.df = pd.read_csv(self.data_file)

        # Convert date column to datetime
        if "month" not in self.df.columns:
            raise ValueError("Expected 'month' column in input data.")
        self.df["month"] = pd.to_datetime(self.df["month"], errors="coerce")

        # Basic validation for required columns
        required = [
            "program_cost",
            "security_incidents",
            "incident_savings",
            "productivity_gain",
            "compliance_savings",
            "total_benefits"
        ]
        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        self.roi_df = None
        self.summary = None

    def calculate_monthly_roi(self):
        """
        Calculate monthly ROI metrics.

        Returns:
            DataFrame with monthly ROI calculations
        """
        df = self.df.copy()

        # Baseline incident costs (constant baseline from generator; fallback if missing)
        if "baseline_incident_cost" in df.columns:
            baseline_incident_cost = df["baseline_incident_cost"]
        else:
            # If baseline not present, estimate baseline using first 3 months avg incidents
            incident_cost_per = 25000
            baseline_incidents_est = int(round(df["security_incidents"].head(3).mean()))
            baseline_incident_cost = baseline_incidents_est * incident_cost_per

        df["baseline_incident_cost"] = baseline_incident_cost

        # Ensure numeric and non-negative values
        df["incident_savings"] = pd.to_numeric(df["incident_savings"], errors="coerce").fillna(0).clip(lower=0)
        df["productivity_gain"] = pd.to_numeric(df["productivity_gain"], errors="coerce").fillna(0).clip(lower=0)
        df["compliance_savings"] = pd.to_numeric(df["compliance_savings"], errors="coerce").fillna(0).clip(lower=0)
        df["program_cost"] = pd.to_numeric(df["program_cost"], errors="coerce").fillna(0).clip(lower=0)

        # Recalculate total benefits to ensure consistency
        df["total_benefits"] = df["incident_savings"] + df["productivity_gain"] + df["compliance_savings"]

        # Net benefits
        df["net_benefits"] = df["total_benefits"] - df["program_cost"]

        # ROI percentage: (net_benefits / costs) * 100
        df["monthly_roi_pct"] = np.where(
            df["program_cost"] > 0,
            (df["net_benefits"] / df["program_cost"]) * 100.0,
            0.0
        )

        self.roi_df = df
        return df

    def calculate_cumulative_roi(self):
        """
        Calculate cumulative ROI over time.

        Returns:
            DataFrame with cumulative metrics
        """
        if self.roi_df is None:
            self.calculate_monthly_roi()

        df = self.roi_df.copy()

        # Cumulative costs, benefits, net
        df["cumulative_costs"] = df["program_cost"].cumsum()
        df["cumulative_benefits"] = df["total_benefits"].cumsum()
        df["cumulative_net_benefits"] = df["net_benefits"].cumsum()

        # Cumulative ROI percentage
        df["cumulative_roi_pct"] = np.where(
            df["cumulative_costs"] > 0,
            (df["cumulative_net_benefits"] / df["cumulative_costs"]) * 100.0,
            0.0
        )

        self.roi_df = df
        return df

    def calculate_payback_period(self):
        """
        Determine when the program breaks even.

        Returns:
            Tuple of (months_to_payback, payback_date)
        """
        if self.roi_df is None or "cumulative_net_benefits" not in self.roi_df.columns:
            self.calculate_cumulative_roi()

        df = self.roi_df
        breakeven = df[df["cumulative_net_benefits"] > 0]

        if breakeven.empty:
            return (None, None)

        first_row = breakeven.iloc[0]
        months_to_payback = int(df.index.get_loc(first_row.name) + 1)  # 1-based months count
        payback_date = first_row["month"].date().isoformat()

        return (months_to_payback, payback_date)

    def generate_roi_summary(self):
        """
        Generate comprehensive ROI summary statistics.

        Returns:
            Dictionary with key ROI metrics
        """
        if self.roi_df is None or "cumulative_roi_pct" not in self.roi_df.columns:
            self.calculate_cumulative_roi()

        df = self.roi_df

        total_investment = float(df["program_cost"].sum())
        total_benefits = float(df["total_benefits"].sum())
        total_net_benefits = float(df["net_benefits"].sum())

        final_roi = float(df["cumulative_roi_pct"].iloc[-1])

        months_to_payback, payback_date = self.calculate_payback_period()

        avg_monthly_roi = float(df["monthly_roi_pct"].mean())
        best_monthly_roi = float(df["monthly_roi_pct"].max())
        worst_monthly_roi = float(df["monthly_roi_pct"].min())

        summary = {
            "total_investment": round(total_investment, 2),
            "total_benefits": round(total_benefits, 2),
            "total_net_benefits": round(total_net_benefits, 2),
            "final_cumulative_roi_pct": round(final_roi, 2),
            "months_to_payback": months_to_payback,
            "payback_date": payback_date,
            "average_monthly_roi_pct": round(avg_monthly_roi, 2),
            "best_monthly_roi_pct": round(best_monthly_roi, 2),
            "worst_monthly_roi_pct": round(worst_monthly_roi, 2),
            "period_months": int(len(df))
        }

        self.summary = summary
        return summary

    def export_results(self, csv_file, json_file):
        """Export detailed results and summary"""
        if self.roi_df is None:
            self.calculate_cumulative_roi()
        if self.summary is None:
            self.generate_roi_summary()

        csv_path = Path(csv_file)
        json_path = Path(json_file)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        self.roi_df.to_csv(csv_path, index=False)
        with open(json_path, "w") as f:
            json.dump(self.summary, f, indent=2)

        print(f"Exported detailed ROI results to: {csv_path.resolve()}")
        print(f"Exported ROI summary to: {json_path.resolve()}")


def main():
    """Main execution function"""
    # Initialize calculator with data file
    calculator = SecurityCultureROICalculator("../data/security_metrics.csv")

    # Calculate all ROI metrics
    calculator.calculate_monthly_roi()
    calculator.calculate_cumulative_roi()

    # Generate and display summary
    summary = calculator.generate_roi_summary()

    print("\n" + "=" * 70)
    print("SECURITY CULTURE PROGRAM ROI SUMMARY")
    print("=" * 70)
    for k, v in summary.items():
        print(f"{k}: {v}")

    # Export results
    calculator.export_results(
        "../reports/roi_detailed_results.csv",
        "../reports/roi_summary.json"
    )


if __name__ == "__main__":
    main()
