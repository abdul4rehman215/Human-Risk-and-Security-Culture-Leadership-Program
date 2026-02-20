#!/usr/bin/env python3
"""
Security Culture Assessment Configuration
Full Implementation (All TODOs completed)
"""

from datetime import datetime

# Assessment metadata
ASSESSMENT_CONFIG = {
    "program_name": "Security Culture Program",
    "organization": "Sample Organization",
    "assessment_period": "2024-Q1",
    "assessment_version": "1.0",
    "assessment_date": datetime.now().strftime("%Y-%m-%d"),
}

# Maturity scoring weights (must sum to 1.0)
CATEGORY_WEIGHTS = {
    "awareness": 0.25,
    "behavior": 0.30,
    "culture": 0.25,
    "outcomes": 0.20
}

# Define maturity level thresholds (0-100)
# Format: {'Level_Name': (min_score, max_score)}
MATURITY_THRESHOLDS = {
    "Initial": (0, 20),
    "Developing": (21, 40),
    "Defined": (41, 60),
    "Managed": (61, 80),
    "Optimizing": (81, 100)
}

# Metrics to collect for each category
METRICS_DEFINITION = {
    "awareness": ["training_completion", "phishing_click_rate", "knowledge_scores"],
    "behavior": ["incident_reporting", "policy_compliance", "security_practices"],
    "culture": ["leadership_support", "employee_engagement", "communication"],
    "outcomes": ["incident_reduction", "response_time", "risk_mitigation"]
}
