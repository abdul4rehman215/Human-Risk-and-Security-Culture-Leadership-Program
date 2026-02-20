#!/usr/bin/env python3
"""
Security Program Benchmarking Analyzer
Students: Complete the TODO sections
"""

import yaml
import pandas as pd
from typing import Dict, Tuple, Any


class BenchmarkAnalyzer:
    def __init__(self, config_path: str, questions_path: str):
        """
        Initialize the analyzer with configuration files.

        Args:
            config_path: Path to framework configuration
            questions_path: Path to questions file
        """
        # Load YAML configuration files
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        with open(questions_path, "r", encoding="utf-8") as f:
            self.questions = yaml.safe_load(f)

        # Initialize instance variables
        self.domains = self.config.get("domains", {})
        self.maturity_levels = self.config.get("maturity_levels", {})
        self.thresholds = self.config.get("scoring", {}).get("thresholds", {})

    def calculate_domain_score(self, domain: str, responses: list) -> float:
        """
        Calculate weighted score for a domain.

        Args:
            domain: Domain name
            responses: List of response scores (1-5)

        Returns:
            Domain score as percentage (0-100)
        """
        domain_questions = self.questions.get(domain, [])
        if not domain_questions:
            return 0.0

        if not responses or len(responses) != len(domain_questions):
            raise ValueError(
                f"Response count mismatch for domain '{domain}'. "
                f"Expected {len(domain_questions)} responses, got {len(responses) if responses else 0}."
            )

        total_weight = sum(float(q.get("weight", 0)) for q in domain_questions)
        if total_weight == 0:
            raise ValueError(f"Total weight is zero for domain '{domain}'")

        weighted_sum = 0.0
        for resp, q in zip(responses, domain_questions):
            w = float(q.get("weight", 0))
            score_1_to_5 = float(resp)

            # Normalize response to percentage: 1->20, 5->100
            percent = (score_1_to_5 / 5.0) * 100.0
            weighted_sum += percent * w

        domain_score = weighted_sum / total_weight
        return round(domain_score, 2)

    def calculate_overall_score(self, domain_scores: Dict[str, float]) -> float:
        """
        Calculate overall maturity score.

        Args:
            domain_scores: Dictionary of domain scores

        Returns:
            Overall weighted score
        """
        total_weight = 0.0
        weighted_sum = 0.0

        for domain, score in domain_scores.items():
            w = float(self.domains.get(domain, {}).get("weight", 0))
            total_weight += w
            weighted_sum += score * w

        if total_weight == 0:
            return 0.0

        overall = weighted_sum / total_weight
        return round(overall, 2)

    def determine_maturity_level(self, score: float) -> Tuple[int, str]:
        """
        Determine maturity level based on score.

        Args:
            score: Overall maturity score

        Returns:
            Tuple of (level_number, level_name)
        """
        critical = float(self.thresholds.get("critical", 60))
        moderate = float(self.thresholds.get("moderate", 75))
        good = float(self.thresholds.get("good", 85))
        excellent = float(self.thresholds.get("excellent", 95))

        if score < critical:
            level = 1
        elif score < moderate:
            level = 2
        elif score < good:
            level = 3
        elif score < excellent:
            level = 4
        else:
            level = 5

        level_name = self.maturity_levels.get(level, "Unknown")
        return level, level_name

    def analyze_assessment(self, responses_path: str) -> dict:
        """
        Perform complete assessment analysis.

        Args:
            responses_path: Path to assessment responses

        Returns:
            Dictionary containing analysis results
        """
        # Load assessment responses
        with open(responses_path, "r", encoding="utf-8") as f:
            assessment = yaml.safe_load(f)

        org_info = assessment.get("organization", {})
        responses = assessment.get("responses", {})

        # Calculate all domain scores
        domain_scores: Dict[str, float] = {}
        for domain in self.domains.keys():
            domain_scores[domain] = self.calculate_domain_score(
                domain,
                responses.get(domain, [])
            )

        # Calculate overall score
        overall_score = self.calculate_overall_score(domain_scores)

        # Determine maturity level
        level_num, level_name = self.determine_maturity_level(overall_score)

        return {
            "organization": org_info,
            "domain_scores": domain_scores,
            "overall_score": overall_score,
            "maturity_level": {
                "level": level_num,
                "name": level_name,
            },
            "framework": self.config.get("framework", {}),
        }
