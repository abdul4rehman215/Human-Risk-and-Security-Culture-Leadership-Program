#!/usr/bin/env python3
"""
Sample Data Generator for Security Culture Assessment
Full Implementation (All TODOs completed)
"""

import json
import random
from pathlib import Path
from datetime import datetime


class DataGenerator:
    def __init__(self, output_dir="data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_training_metrics(self):
        """
        Generate sample training and awareness metrics
        Returns: dict
        """
        total_employees = 500

        # Completion rate realistic: 70% to 95%
        completion_rate = round(random.uniform(70, 95), 2)
        training_completed = int(total_employees * (completion_rate / 100))

        # Average score realistic: 65 to 92
        average_score = round(random.uniform(65, 92), 2)

        # Satisfaction rating realistic: 3.2 to 4.8 (1-5 scale)
        satisfaction_rating = round(random.uniform(3.2, 4.8), 2)

        metrics = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_employees": total_employees,
            "training_completed": training_completed,
            "completion_rate": completion_rate,
            "average_score": average_score,
            "satisfaction_rating": satisfaction_rating
        }
        return metrics

    def generate_phishing_metrics(self):
        """
        Generate phishing simulation results
        Returns: dict
        """
        campaigns_sent = random.randint(3, 6)
        total_emails = random.randint(2000, 4000)

        # Click rate realistic: 4% to 16%
        click_rate = round(random.uniform(4.0, 16.0), 2)
        clicked_links = int(total_emails * (click_rate / 100))

        # Reporting rate realistic: 20% to 65%
        reporting_rate = round(random.uniform(20.0, 65.0), 2)
        reported_suspicious = int(total_emails * (reporting_rate / 100))

        metrics = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campaigns_sent": campaigns_sent,
            "total_emails": total_emails,
            "clicked_links": clicked_links,
            "click_rate": click_rate,
            "reported_suspicious": reported_suspicious,
            "reporting_rate": reporting_rate
        }
        return metrics

    def generate_incident_metrics(self):
        """
        Generate incident reporting and response metrics
        Returns: dict
        """
        total_incidents = random.randint(18, 55)

        # Self-reported typically 25% to 60%
        self_reporting_rate = round(random.uniform(25.0, 60.0), 2)
        self_reported = int(total_incidents * (self_reporting_rate / 100))

        # Response time in hours: 2 to 48 hours
        average_response_time = round(random.uniform(2.0, 48.0), 2)

        # Resolution rate: 80% to 98%
        resolution_rate = round(random.uniform(80.0, 98.0), 2)
        resolved_incidents = int(total_incidents * (resolution_rate / 100))

        metrics = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_incidents": total_incidents,
            "self_reported": self_reported,
            "self_reporting_rate": self_reporting_rate,
            "average_response_time_hours": average_response_time,
            "resolved_incidents": resolved_incidents,
            "resolution_rate": resolution_rate
        }
        return metrics

    def generate_compliance_metrics(self):
        """
        Generate policy compliance metrics
        Returns: dict
        """
        # Realistic policy compliance: 70% to 97%
        policy_compliance_rate = round(random.uniform(70.0, 97.0), 2)

        # Security practices: score out of 100, 55-92
        security_practices_score = round(random.uniform(55.0, 92.0), 2)

        metrics = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "policy_compliance_rate": policy_compliance_rate,
            "security_practices_score": security_practices_score
        }
        return metrics

    def generate_leadership_culture_metrics(self):
        """
        Generate leadership support + engagement culture metrics
        Returns: dict
        """
        # Leadership support score: 50-95
        leadership_support_score = round(random.uniform(50.0, 95.0), 2)

        # Employee engagement score: 45-90
        employee_engagement_score = round(random.uniform(45.0, 90.0), 2)

        # Communication effectiveness score: 40-88
        communication_score = round(random.uniform(40.0, 88.0), 2)

        metrics = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "leadership_support_score": leadership_support_score,
            "employee_engagement_score": employee_engagement_score,
            "communication_score": communication_score
        }
        return metrics

    def generate_culture_survey(self, num_responses=100):
        """
        Generate employee culture survey responses (1-5 scale)
        Returns: list
        """
        responses = []

        departments = ["IT", "Finance", "HR", "Sales", "Marketing", "Operations"]
        roles = ["Analyst", "Manager", "Executive", "Engineer", "Coordinator", "Specialist"]
        tenure_buckets = ["<1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]

        questions = [
            "Security is a priority in our organization",
            "Leadership demonstrates commitment to security",
            "I feel comfortable reporting security concerns",
            "Security training is relevant and useful"
        ]

        # Simulate realistic distribution: mostly 3-5, fewer 1-2
        rating_pool = [1, 2, 3, 3, 3, 4, 4, 4, 5, 5]

        for i in range(num_responses):
            entry = {
                "response_id": f"R{i+1:03d}",
                "department": random.choice(departments),
                "role": random.choice(roles),
                "tenure": random.choice(tenure_buckets),
                "answers": {}
            }

            for q in questions:
                entry["answers"][q] = random.choice(rating_pool)

            responses.append(entry)

        return responses

    def save_all_data(self):
        """
        Generate and save all assessment data files
        """
        training = self.generate_training_metrics()
        phishing = self.generate_phishing_metrics()
        incidents = self.generate_incident_metrics()
        compliance = self.generate_compliance_metrics()
        culture = self.generate_leadership_culture_metrics()
        survey = self.generate_culture_survey(120)

        datasets = {
            "training_metrics.json": training,
            "phishing_metrics.json": phishing,
            "incident_metrics.json": incidents,
            "compliance_metrics.json": compliance,
            "culture_metrics.json": culture,
            "survey_responses.json": survey
        }

        for filename, data in datasets.items():
            file_path = self.output_dir / filename
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[+] Created {file_path}")

        print("\nAll assessment datasets generated successfully!")


if __name__ == "__main__":
    generator = DataGenerator()
    generator.save_all_data()
