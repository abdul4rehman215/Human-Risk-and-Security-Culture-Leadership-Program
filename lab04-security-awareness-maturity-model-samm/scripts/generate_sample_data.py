#!/usr/bin/env python3
"""
Sample Survey Data Generator for SAMM Assessment
Students: Complete the TODO sections to generate realistic survey data
"""

import csv
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any


def generate_sample_responses(num_responses: int = 50) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Generate sample survey responses for SAMM assessment.

    Args:
        num_responses: Number of survey responses to generate

    Returns:
        Tuple of (responses list, questions dictionary)
    """

    # Define survey questions
    questions = {
        # Governance category questions
        "governance_policy_framework": "Rate security policy framework (1-5)",
        "governance_leadership_commitment": "Rate leadership commitment to security awareness (1-5)",
        "governance_resource_allocation": "Rate resource allocation for awareness/training (1-5)",
        "governance_compliance_monitoring": "Rate compliance monitoring and enforcement (1-5)",

        # Training category questions
        "training_awareness_programs": "Rate awareness programs (1-5)",
        "training_role_based_training": "Rate role-based security training (1-5)",
        "training_training_effectiveness": "Rate training effectiveness (knowledge retention) (1-5)",
        "training_continuous_learning": "Rate continuous learning opportunities (1-5)",

        # Culture category questions
        "culture_behavioral_change": "Rate observed behavioral change in security practices (1-5)",
        "culture_incident_reporting": "Rate incident reporting culture and ease (1-5)",
        "culture_peer_influence": "Rate positive peer influence on secure behavior (1-5)",
        "culture_recognition_programs": "Rate recognition programs for secure behavior (1-5)",

        # Measurement category questions
        "measurement_kpi_tracking": "Rate KPI tracking for security awareness (1-5)",
        "measurement_assessment_frequency": "Rate how often awareness is assessed (1-5)",
        "measurement_data_analysis": "Rate depth of analysis performed on awareness data (1-5)",
        "measurement_improvement_actions": "Rate effectiveness of improvement actions taken (1-5)",
    }

    responses: List[Dict[str, Any]] = []

    departments = ["IT", "HR", "Finance", "Marketing", "Operations"]
    role_levels = ["Junior", "Mid", "Senior", "Manager", "Executive"]

    # Choose a base maturity for the whole organization to create correlated data
    # This simulates an org that is around 2-4 maturity on average
    org_base = random.choice([2, 3, 3, 4])

    for i in range(num_responses):
        dept = random.choice(departments)
        role = random.choice(role_levels)
        years_exp = random.randint(0, 15)

        # Department maturity bias (example)
        dept_bias = 0
        if dept == "IT":
            dept_bias = 0.6
        elif dept == "Finance":
            dept_bias = 0.3
        elif dept == "HR":
            dept_bias = 0.1
        elif dept == "Marketing":
            dept_bias = -0.1
        elif dept == "Operations":
            dept_bias = -0.2

        # Role bias (example)
        role_bias = 0
        if role in ["Senior", "Manager"]:
            role_bias = 0.3
        elif role == "Executive":
            role_bias = 0.2
        elif role == "Junior":
            role_bias = -0.2

        # Experience bias (small)
        exp_bias = min(0.4, years_exp / 30.0)

        base = org_base + dept_bias + role_bias + exp_bias
        # clamp base to 1..5
        if base < 1:
            base = 1
        if base > 5:
            base = 5

        response = {
            "response_id": f"RESP_{i+1:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "department": dept,
            "role_level": role,
            "years_experience": years_exp,
        }

        # Generate realistic scores for each question (1-5) using correlated base + noise
        for qkey in questions.keys():
            noise = random.uniform(-0.8, 0.8)
            score = round(base + noise)

            if score < 1:
                score = 1
            if score > 5:
                score = 5

            response[qkey] = score

        responses.append(response)

    return responses, questions


def save_sample_data(filename: str, responses: List[Dict[str, Any]], questions: Dict[str, str]) -> bool:
    """
    Save sample data to CSV file.

    Args:
        filename: Output CSV filename
        responses: List of response dictionaries
        questions: Dictionary of questions

    Returns:
        Boolean indicating success
    """
    try:
        # Create CSV writer with appropriate fieldnames
        fieldnames = ["response_id", "timestamp", "department", "role_level", "years_experience"] + list(questions.keys())

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Write all responses
            for r in responses:
                writer.writerow(r)

        print(f"Sample data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


if __name__ == "__main__":
    # Generate 75 sample responses
    responses, questions = generate_sample_responses(num_responses=75)

    # Save to ../data/sample_survey_data.csv
    save_sample_data("../data/sample_survey_data.csv", responses, questions)
