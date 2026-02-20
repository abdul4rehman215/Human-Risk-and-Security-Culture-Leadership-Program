#!/usr/bin/env python3
"""
Sample Data Generator
Generate realistic compliance and impact metrics
"""
import pandas as pd
import numpy as np
import random


class MetricsDataGenerator:
    def __init__(self):
        self.departments = ["IT", "Finance", "HR", "Sales", "Marketing", "Operations"]
        self.months = 12

    def _month_index(self):
        end = pd.Timestamp.today().normalize().replace(day=1)
        return pd.date_range(end=end, periods=self.months, freq="MS")

    def generate_compliance_data(self):
        dates = self._month_index()

        dept_sizes = {
            "IT": random.randint(40, 80),
            "Finance": random.randint(30, 70),
            "HR": random.randint(15, 40),
            "Sales": random.randint(50, 120),
            "Marketing": random.randint(25, 60),
            "Operations": random.randint(60, 160),
        }

        rows = []
        np.random.seed(42)

        for d in dates:
            seasonal_boost = 0.01 if d.month in (11, 12) else 0.0

            for dept in self.departments:
                size = dept_sizes[dept]

                if dept in ("IT", "Finance"):
                    base_training, base_policy, base_assess, base_phish = 0.88, 0.90, 0.86, 0.10
                elif dept in ("HR", "Marketing"):
                    base_training, base_policy, base_assess, base_phish = 0.85, 0.87, 0.83, 0.12
                else:
                    base_training, base_policy, base_assess, base_phish = 0.80, 0.84, 0.78, 0.14

                t = (d - dates[0]).days / 30.0
                improvement = 0.03 * (1 - np.exp(-0.25 * t))

                training = np.clip(base_training + improvement + seasonal_boost + np.random.normal(0, 0.015), 0.70, 0.99)
                policy = np.clip(base_policy + improvement + seasonal_boost + np.random.normal(0, 0.012), 0.70, 0.99)
                assess = np.clip(base_assess + improvement + np.random.normal(0, 0.018), 0.70, 0.99)
                phish = np.clip(base_phish - 0.04 * (1 - np.exp(-0.18 * t)) + np.random.normal(0, 0.01), 0.03, 0.30)

                compliance_score = (training + policy + assess + (1 - phish)) / 4.0

                rows.append({
                    "date": d.strftime("%Y-%m"),
                    "department": dept,
                    "department_size": size,
                    "training_completion_rate": round(training * 100, 2),
                    "policy_acknowledgment_rate": round(policy * 100, 2),
                    "phishing_click_rate": round(phish * 100, 2),
                    "assessment_pass_rate": round(assess * 100, 2),
                    "compliance_score": round(compliance_score * 100, 2),
                })

        df = pd.DataFrame(rows)
        df.to_csv("compliance_metrics.csv", index=False)
        print("Saved: compliance_metrics.csv")
        return df

    def generate_impact_data(self):
        dates = self._month_index()
        rows = []
        np.random.seed(100)

        base = {
            "IT": {"reports": 8, "discuss": 18, "proactive": 25, "coach": 10, "incidents": 7, "maturity": 62},
            "Finance": {"reports": 6, "discuss": 14, "proactive": 18, "coach": 7, "incidents": 8, "maturity": 58},
            "HR": {"reports": 4, "discuss": 12, "proactive": 15, "coach": 6, "incidents": 6, "maturity": 55},
            "Sales": {"reports": 3, "discuss": 10, "proactive": 12, "coach": 4, "incidents": 10, "maturity": 48},
            "Marketing": {"reports": 4, "discuss": 11, "proactive": 14, "coach": 5, "incidents": 7, "maturity": 52},
            "Operations": {"reports": 5, "discuss": 13, "proactive": 16, "coach": 6, "incidents": 9, "maturity": 50},
        }

        for d in dates:
            t = (d - dates[0]).days / 30.0
            maturity_gain = 20 * (1 - np.exp(-0.12 * t))
            behavior_gain = 0.6 * (1 - np.exp(-0.15 * t))
            incident_reduction = 0.45 * (1 - np.exp(-0.18 * t))

            for dept in self.departments:
                b = base[dept]

                voluntary = int(max(0, round(b["reports"] * (1 + behavior_gain) + np.random.normal(0, 1.2))))
                discussions = int(max(0, round(b["discuss"] * (1 + behavior_gain) + np.random.normal(0, 2.0))))
                proactive = int(max(0, round(b["proactive"] * (1 + behavior_gain) + np.random.normal(0, 2.2))))
                coaching = int(max(0, round(b["coach"] * (1 + behavior_gain) + np.random.normal(0, 1.3))))
                incidents = int(max(0, round(b["incidents"] * (1 - incident_reduction) + np.random.normal(0, 1.0))))
                maturity = float(np.clip(b["maturity"] + maturity_gain + np.random.normal(0, 2.0), 0, 100))

                rows.append({
                    "date": d.strftime("%Y-%m"),
                    "department": dept,
                    "voluntary_incident_reports": voluntary,
                    "security_discussions_initiated": discussions,
                    "proactive_security_behaviors": proactive,
                    "peer_coaching_instances": coaching,
                    "security_incidents": incidents,
                    "culture_maturity_score": round(maturity, 2),
                })

        df = pd.DataFrame(rows)
        df.to_csv("impact_metrics.csv", index=False)
        print("Saved: impact_metrics.csv")
        return df

    def save_datasets(self):
        self.generate_compliance_data()
        self.generate_impact_data()
        print("Sample datasets created successfully!")


if __name__ == "__main__":
    generator = MetricsDataGenerator()
    generator.save_datasets()
