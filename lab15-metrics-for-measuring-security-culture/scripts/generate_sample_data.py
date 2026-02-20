import sqlite3
import random
from datetime import datetime, timedelta


def random_date_within(days_back=365):
    """Return ISO date string within last N days."""
    d = datetime.utcnow() - timedelta(days=random.randint(0, days_back))
    return d.strftime("%Y-%m-%d")


def generate_sample_data():
    """
    Generate realistic sample data for testing.

    - Generate 100 employees across 6 departments
    - Create 2-6 training records per employee
    - Create 3-8 phishing simulation records per employee
    - Create 50 security incidents
    - Create 1-3 survey responses per employee
    """
    conn = sqlite3.connect('data/security_culture.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Operations', 'Sales']
    roles_by_dept = {
        'IT': ['System Admin', 'Developer', 'Security Analyst', 'Network Engineer'],
        'HR': ['HR Specialist', 'Recruiter', 'HR Manager'],
        'Finance': ['Accountant', 'Financial Analyst', 'Controller'],
        'Marketing': ['Marketing Specialist', 'Content Strategist', 'Marketing Manager'],
        'Operations': ['Operations Manager', 'Project Manager', 'Quality Analyst'],
        'Sales': ['Sales Rep', 'Account Executive', 'Sales Manager']
    }
    training_types = ['Security Awareness', 'Phishing Awareness', 'Password Hygiene', 'Data Handling', 'Incident Reporting']
    incident_types = ['Phishing', 'Malware', 'Policy Violation', 'Lost Device', 'Unauthorized Access', 'Data Exposure']
    severities = ['Low', 'Medium', 'High', 'Critical']

    # Clear existing data to avoid duplicates
    cursor.execute("DELETE FROM security_training;")
    cursor.execute("DELETE FROM phishing_simulations;")
    cursor.execute("DELETE FROM security_incidents;")
    cursor.execute("DELETE FROM security_surveys;")
    cursor.execute("DELETE FROM employees;")
    conn.commit()

    # Generate employee data
    employees = []
    for i in range(1, 101):
        emp_id = f"EMP{i:03d}"
        dept = random.choice(departments)
        role = random.choice(roles_by_dept[dept])
        hire_date = (datetime.utcnow() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d")
        employees.append((emp_id, dept, role, hire_date))

    cursor.executemany("""
        INSERT INTO employees (employee_id, department, role, hire_date)
        VALUES (?, ?, ?, ?);
    """, employees)

    # Generate training completion data
    training_rows = []
    for (emp_id, dept, role, hire_date) in employees:
        num_records = random.randint(2, 6)
        for _ in range(num_records):
            ttype = random.choice(training_types)
            completion_date = random_date_within(days_back=365)

            base = 78
            if dept == "IT":
                base = 82
            if dept == "Sales":
                base = 75

            score = int(min(100, max(40, random.gauss(base, 10))))
            training_rows.append((emp_id, ttype, completion_date, score))

    cursor.executemany("""
        INSERT INTO security_training (employee_id, training_type, completion_date, score)
        VALUES (?, ?, ?, ?);
    """, training_rows)

    # Generate phishing simulation results
    phishing_rows = []
    for (emp_id, dept, role, hire_date) in employees:
        num_sims = random.randint(3, 8)
        for _ in range(num_sims):
            sim_date = random_date_within(days_back=365)

            click_prob = 0.12
            report_prob = 0.55

            if dept == "IT":
                click_prob = 0.07
                report_prob = 0.65
            elif dept == "Finance":
                click_prob = 0.10
                report_prob = 0.60
            elif dept == "Sales":
                click_prob = 0.18
                report_prob = 0.45

            clicked = 1 if random.random() < click_prob else 0
            adjusted_report_prob = report_prob - (0.10 if clicked else 0.0)
            reported = 1 if random.random() < max(0.05, adjusted_report_prob) else 0

            phishing_rows.append((emp_id, sim_date, clicked, reported))

    cursor.executemany("""
        INSERT INTO phishing_simulations (employee_id, simulation_date, clicked_link, reported_email)
        VALUES (?, ?, ?, ?);
    """, phishing_rows)

    # Generate security incidents
    incident_rows = []
    for _ in range(50):
        incident_date = random_date_within(days_back=365)
        itype = random.choice(incident_types)
        severity = random.choices(severities, weights=[50, 30, 15, 5], k=1)[0]

        if random.random() < 0.15:
            emp_id = None
        else:
            emp_id = random.choice(employees)[0]

        incident_rows.append((emp_id, incident_date, itype, severity))

    cursor.executemany("""
        INSERT INTO security_incidents (employee_id, incident_date, incident_type, severity)
        VALUES (?, ?, ?, ?);
    """, incident_rows)

    # Generate survey responses
    survey_rows = []
    for (emp_id, dept, role, hire_date) in employees:
        num_surveys = random.randint(1, 3)
        for _ in range(num_surveys):
            survey_date = random_date_within(days_back=365)

            aw_base = 7
            beh_base = 7
            if dept == "IT":
                aw_base = 8
                beh_base = 8
            if dept == "Sales":
                aw_base = 6
                beh_base = 6

            awareness_score = int(min(10, max(1, round(random.gauss(aw_base, 1.3)))))
            behavior_score = int(min(10, max(1, round(random.gauss(beh_base, 1.4)))))

            survey_rows.append((emp_id, survey_date, awareness_score, behavior_score))

    cursor.executemany("""
        INSERT INTO security_surveys (employee_id, survey_date, awareness_score, behavior_score)
        VALUES (?, ?, ?, ?);
    """, survey_rows)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    generate_sample_data()
    print("Sample data generated in data/security_culture.db")
