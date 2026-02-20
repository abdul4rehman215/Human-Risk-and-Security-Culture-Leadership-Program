#!/usr/bin/env python3
"""
Employee Data Generator for Security Training Segmentation
Complete implementation version
"""

import csv
import random


def _risk_points_access(access_level: str) -> int:
    access_map = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }
    return access_map.get(access_level, 2)


def _risk_points_training(last_training: str) -> int:
    # More time since training -> higher risk
    training_map = {
        "Within 3 months": 1,
        "6-12 months ago": 2,
        "Over 1 year ago": 3,
        "Never": 4,
    }
    return training_map.get(last_training, 3)


def _risk_points_incident(incident_history: str) -> int:
    incident_map = {
        "None": 0,
        "Minor": 1,
        "Moderate": 2,
        "Severe": 3,
    }
    return incident_map.get(incident_history, 1)


def _department_risk_adjustment(department: str) -> int:
    """
    Department-specific risk adjustments:
    - IT: higher exposure/privileges
    - Finance/Legal/Executive: sensitive data/decision impact
    - Others: moderate
    """
    adjustments = {
        "IT": 2,
        "Finance": 2,
        "Legal": 1,
        "Executive": 2,
        "HR": 1,
        "Operations": 1,
        "Marketing": 0,
    }
    return adjustments.get(department, 0)


def generate_employee_data(num_employees=200):
    """
    Generate sample employee data with security-relevant attributes.

    Risk score range: 1-12
    """

    departments = ["IT", "Finance", "HR", "Marketing", "Operations", "Legal", "Executive"]

    roles = {
        "IT": ["System Administrator", "Developer", "Security Analyst", "Network Engineer"],
        "Finance": ["Accountant", "Financial Analyst", "Controller", "CFO"],
        "HR": ["HR Specialist", "Recruiter", "HR Manager", "Benefits Coordinator"],
        "Marketing": ["Marketing Specialist", "Content Creator", "Marketing Manager"],
        "Operations": ["Operations Manager", "Project Manager", "Quality Analyst"],
        "Legal": ["Legal Counsel", "Compliance Officer", "Contract Manager"],
        "Executive": ["CEO", "CTO", "VP Sales", "VP Operations"],
    }

    locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    access_levels = ["Low", "Medium", "High", "Critical"]
    training_history = ["Never", "Over 1 year ago", "6-12 months ago", "Within 3 months"]
    incident_history = ["None", "Minor", "Moderate", "Severe"]

    employees = []

    for i in range(1, num_employees + 1):
        dept = random.choice(departments)

        access = random.choice(access_levels)
        training = random.choice(training_history)
        incident = random.choice(incident_history)

        base = (
            _risk_points_access(access)
            + _risk_points_training(training)
            + _risk_points_incident(incident)
        )

        adjusted = base + _department_risk_adjustment(dept)

        # Normalize risk score between 1 and 12
        risk_score = max(1, min(12, adjusted))

        employee = {
            "employee_id": f"EMP{i:03d}",
            "name": f"Employee {i}",
            "department": dept,
            "role": random.choice(roles[dept]),
            "location": random.choice(locations),
            "access_level": access,
            "last_training": training,
            "incident_history": incident,
            "years_experience": random.randint(1, 20),
            "risk_score": risk_score,
        }

        employees.append(employee)

    return employees


def save_to_csv(employees, filename="employees.csv"):
    """
    Save employee data to CSV file.
    """
    if not employees:
        raise ValueError("No employee data provided to save.")

    fieldnames = list(employees[0].keys())

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)


if __name__ == "__main__":
    print("Generating employee data...")
    employees = generate_employee_data(200)
    save_to_csv(employees, "employees.csv")
    print("Done! Generated 200 employee records and saved to employees.csv")
