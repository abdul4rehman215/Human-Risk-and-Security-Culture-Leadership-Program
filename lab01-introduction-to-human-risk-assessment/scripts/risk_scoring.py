#!/usr/bin/env python3
"""
Human Risk Assessment Scoring System

This script calculates category scores and an overall score (0-100).
Higher score => lower risk (better security posture), based on lab thresholds:
- 80-100: Low Risk
- 60-79 : Medium Risk
- 40-59 : High Risk
- 0-39  : Critical Risk
"""

import sqlite3
from typing import Dict, List, Tuple, Any


class RiskScorer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Category weights must sum to 1.0
        self.risk_weights: Dict[str, float] = {
            "password_security": 0.25,
            "email_security": 0.20,
            "social_engineering": 0.20,
            "device_security": 0.15,
            "training_awareness": 0.20,
        }

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def calculate_category_score(self, responses: List[Dict[str, Any]], category: str) -> int:
        """
        Calculate score for a specific category.
        Assumes response_value is on a 1-5 scale.
        Returns integer score 0-100.
        """
        cat_values = [r["response_value"] for r in responses if r["category"] == category]

        if not cat_values:
            return 0

        avg_val = sum(cat_values) / len(cat_values)
        normalized = int(round(((avg_val - 1) / 4) * 100))

        if normalized < 0:
            normalized = 0
        if normalized > 100:
            normalized = 100

        return normalized

    def calculate_overall_risk(self, category_scores: Dict[str, int]) -> int:
        total = 0.0
        for category, weight in self.risk_weights.items():
            score = category_scores.get(category, 0)
            total += score * weight

        overall = int(round(total))

        if overall < 0:
            overall = 0
        if overall > 100:
            overall = 100

        return overall

    def get_risk_level(self, score: int) -> str:
        if score >= 80:
            return "Low Risk"
        if score >= 60:
            return "Medium Risk"
        if score >= 40:
            return "High Risk"
        return "Critical Risk"

    def process_participant_scores(self, participant_id: int) -> Tuple[Dict[str, int], int]:
        conn = self._connect()
        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT question_id, response_value, category
                FROM risk_responses
                WHERE participant_id = ?
                """,
                (participant_id,),
            )
            rows = cur.fetchall()
            responses = [{"question_id": q, "response_value": int(v), "category": c} for (q, v, c) in rows]

            category_scores: Dict[str, int] = {}
            for category in self.risk_weights.keys():
                category_scores[category] = self.calculate_category_score(responses, category)

            overall_score = self.calculate_overall_risk(category_scores)

            cur.execute("DELETE FROM risk_scores WHERE participant_id = ?", (participant_id,))

            for category, score in category_scores.items():
                cur.execute(
                    """
                    INSERT INTO risk_scores (participant_id, category, score, risk_level)
                    VALUES (?, ?, ?, ?)
                    """,
                    (participant_id, category, score, self.get_risk_level(score)),
                )

            cur.execute(
                """
                INSERT INTO risk_scores (participant_id, category, score, risk_level)
                VALUES (?, 'overall', ?, ?)
                """,
                (participant_id, overall_score, self.get_risk_level(overall_score)),
            )

            conn.commit()
            return category_scores, overall_score
        finally:
            conn.close()


if __name__ == "__main__":
    scorer = RiskScorer("../data/assessment.db")
    print("Risk scoring system initialized")
