# SAMM Configuration File

# Maturity Levels (0-5 scale)
MATURITY_LEVELS = {
    0: "Non-existent",
    1: "Initial/Ad-hoc",
    2: "Repeatable",
    3: "Defined",
    4: "Managed",
    5: "Optimizing"
}

# Assessment Categories with weights
ASSESSMENT_CATEGORIES = {
    "governance": {
        "name": "Security Governance",
        "weight": 0.25,
        "subcategories": [
            "policy_framework",
            "leadership_commitment",
            "resource_allocation",
            "compliance_monitoring"
        ]
    },
    "training": {
        "name": "Security Training & Education",
        "weight": 0.30,
        "subcategories": [
            "awareness_programs",
            "role_based_training",
            "training_effectiveness",
            "continuous_learning"
        ]
    },
    "culture": {
        "name": "Security Culture",
        "weight": 0.25,
        "subcategories": [
            "behavioral_change",
            "incident_reporting",
            "peer_influence",
            "recognition_programs"
        ]
    },
    "measurement": {
        "name": "Measurement & Metrics",
        "weight": 0.20,
        "subcategories": [
            "kpi_tracking",
            "assessment_frequency",
            "data_analysis",
            "improvement_actions"
        ]
    }
}

# Scoring thresholds for maturity levels
SCORING_THRESHOLDS = {
    5: 4.5,  # Optimizing
    4: 3.5,  # Managed
    3: 2.5,  # Defined
    2: 1.5,  # Repeatable
    1: 0.5,  # Initial
    0: 0.0   # Non-existent
}
