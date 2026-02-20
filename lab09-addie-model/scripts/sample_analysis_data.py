#!/usr/bin/env python3
"""
Generate sample analysis data for testing
"""

import json
import os
from datetime import datetime


def generate_sample_data():
    """Generate sample analysis data for security training"""

    sample = {
        "needs_assessment": {
            "performance_gaps": [
                "High phishing click rates",
                "Weak password practices",
                "Poor incident reporting",
            ],
            "business_objectives": [
                "Reduce security incidents by 40%",
                "Improve compliance scores",
                "Strengthen security culture",
            ],
            "priority": "High",
        },
        "learner_analysis": {
            "demographics": {
                "roles": ["Office Staff", "Managers", "IT Personnel"],
                "experience_level": "Mixed",
                "department": "All",
            },
            "preferences": {
                "methods": ["Interactive", "Visual", "Scenario-based"],
                "technology_comfort": "Medium",
            },
            "constraints": {
                "time_available": "2-3 hours",
                "location": "Online"
            },
        },
        "goals": {
            "learning_goals": [
                "Identify phishing attempts",
                "Create strong passwords",
                "Follow secure practices",
                "Report incidents properly",
            ],
            "success_metrics": [
                "Phishing click rate < 10%",
                "Password compliance > 90%",
                "Training completion > 95%",
            ],
            "timeline_weeks": 4,
        },
        "constraints": {
            "budget": 15000,
            "resources": ["LMS", "SMEs", "Consultant"],
            "technology": "Cross-platform required",
            "compliance": ["SOX", "HIPAA"],
        },
    }

    # Save to file
    os.makedirs("data", exist_ok=True)
    filename = f"data/sample_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(sample, f, indent=4)

    # Print confirmation
    print(f"Sample analysis data saved to: {filename}")

    return sample


if __name__ == "__main__":
    generate_sample_data()
