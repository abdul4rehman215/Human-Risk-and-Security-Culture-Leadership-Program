#!/usr/bin/env python3
"""
Sample Data Generator

Generates sample participants and survey responses for testing.
Inserts into SQLite database:
- participants
- risk_responses
"""

import sqlite3
import random
import string
from typing import Dict


def connect_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def random_employee_id() -> str:
    return "EMP-" + "".join(random.choices(string.digits, k=4))


def generate_sample_data(db_path: str, num_participants: int = 20) -> None:
    conn = connect_db(db_path)
    cur = conn.cursor()

    departments = ["IT", "HR", "Finance", "Marketing", "Operations"]
    roles = ["Manager", "Analyst", "Specialist", "Coordinator"]

    question_categories: Dict[str, str] = {
        "password_unique": "password_security",
        "password_manager": "password_security",
        "email_sender_check": "email_security",
        "email_report": "email_security",
        "phishing_recognition": "social_engineering",
        "info_disclosure": "social_engineering",
        "prompt_updates": "device_security",
        "approved_software": "device_security",
        "training_completed": "training_awareness",
        "policy_familiarity": "training_awareness",
    }

    def insert_participant(employee_id: str, department: str, role: str, experience_years: int) -> int:
        while True:
            try:
                cur.execute(
                    """
                    INSERT INTO participants (employee_id, department, role, experience_years)
                    VALUES (?, ?, ?, ?)
                    """,
                    (employee_id, department, role, experience_years),
                )
                conn.commit()
                return cur.lastrowid
            except sqlite3.IntegrityError:
                employee_id = random_employee_id()

    def insert_response(participant_id: int, question_id: str, response_value: int, category: str) -> None:
        cur.execute(
            """
            INSERT INTO risk_responses (participant_id, question_id, response_value, category)
            VALUES (?, ?, ?, ?)
            """,
            (participant_id, question_id, response_value, category),
        )

    for _ in range(num_participants):
        employee_id = random_employee_id()
        department = random.choice(departments)
        role = random.choice(roles)
        experience_years = random.randint(1, 15)

        participant_id = insert_participant(employee_id, department, role, experience_years)

        for qid, cat in question_categories.items():
            if qid == "training_completed":
                response_value = random.choice([1, 3, 5])
            else:
                response_value = random.randint(1, 5)

            insert_response(participant_id, qid, response_value, cat)

        conn.commit()

    conn.close()
    print(f"Generated sample data for {num_participants} participants")


if __name__ == "__main__":
    db_path = "../data/assessment.db"
    generate_sample_data(db_path)
