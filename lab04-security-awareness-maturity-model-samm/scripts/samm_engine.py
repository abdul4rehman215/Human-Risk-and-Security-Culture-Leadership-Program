#!/usr/bin/env python3
"""
SAMM Assessment Engine
Students: Complete the assessment logic and scoring calculations
"""

import json
import csv
import statistics
import sys
import os

# Make config importable (config/samm_config.py)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))
from samm_config import MATURITY_LEVELS, ASSESSMENT_CATEGORIES, SCORING_THRESHOLDS  # noqa: E402


class SAMMAssessment:
    def __init__(self):
        self.assessment_data = {}
        self.results = {}
        self.recommendations = []

    def load_survey_data(self, csv_file):
        """
        Load survey data from CSV file.

        Args:
            csv_file: Path to CSV file containing survey responses

        Returns:
            List of survey response dictionaries
        """
        # Implement CSV file reading
        # Handle file not found errors
        # Return list of response dictionaries
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Survey data file not found: {csv_file}")

        responses = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert score fields to int when possible
                converted = {}
                for k, v in row.items():
                    if v is None:
                        converted[k] = ""
                        continue
                    v_str = str(v).strip()
                    if v_str.isdigit():
                        converted[k] = int(v_str)
                    else:
                        # also try float->int conversion if needed
                        try:
                            if "." in v_str:
                                converted[k] = float(v_str)
                            else:
                                converted[k] = v_str
                        except Exception:
                            converted[k] = v_str
                responses.append(converted)

        return responses

    def calculate_category_score(self, responses, category):
        """
        Calculate maturity score for a specific category.

        Args:
            responses: List of survey responses
            category: Category key (governance, training, culture, measurement)

        Returns:
            Float representing average category score
        """
        # Extract subcategories for the given category
        cat_info = ASSESSMENT_CATEGORIES.get(category, {})
        subcats = cat_info.get("subcategories", [])

        if not subcats:
            return 0.0

        # Calculate average score for each subcategory
        sub_scores = []
        for sub in subcats:
            col = f"{category}_{sub}"
            values = []
            for r in responses:
                val = r.get(col, "")
                try:
                    val_num = float(val)
                    values.append(val_num)
                except Exception:
                    continue
            if values:
                sub_scores.append(statistics.mean(values))
            else:
                sub_scores.append(0.0)

        # Return overall category average
        if sub_scores:
            return float(round(statistics.mean(sub_scores), 2))
        return 0.0

    def assess_maturity_level(self, score):
        """
        Determine maturity level based on score.

        Args:
            score: Numeric score (0-5 scale)

        Returns:
            Tuple of (level_number, level_name)
        """
        # Compare score against SCORING_THRESHOLDS
        # Return appropriate maturity level and name
        # SCORING_THRESHOLDS maps: level -> minimum score
        for level in sorted(SCORING_THRESHOLDS.keys(), reverse=True):
            threshold = SCORING_THRESHOLDS[level]
            if score >= threshold:
                return level, MATURITY_LEVELS.get(level, "Unknown")
        return 0, MATURITY_LEVELS.get(0, "Non-existent")

    def generate_recommendations(self, category, score, level):
        """
        Generate improvement recommendations based on maturity level.

        Args:
            category: Category key
            score: Current score
            level: Current maturity level

        Returns:
            List of recommendation strings
        """
        # Define recommendations for each category and level
        # Return appropriate recommendations for next level
        # Handle case where already at highest level
        cat_name = ASSESSMENT_CATEGORIES[category]["name"]
        recs = []

        if level >= 5:
            recs.append(f"{cat_name}: Maintain and optimize continuously; mentor other teams and refine metrics.")
            return recs

        next_level = level + 1
        next_name = MATURITY_LEVELS.get(next_level, "Next Level")

        if category == "governance":
            if next_level == 1:
                recs.append("Establish basic security awareness governance ownership and define responsibilities.")
            elif next_level == 2:
                recs.append("Create repeatable policy communication and ensure policies are accessible and acknowledged.")
            elif next_level == 3:
                recs.append("Formalize leadership commitment and embed awareness goals into management objectives.")
            elif next_level == 4:
                recs.append("Implement measurable governance KPIs and regular compliance monitoring reviews.")
            elif next_level == 5:
                recs.append("Continuously improve governance by benchmarking and conducting maturity reassessments.")
        elif category == "training":
            if next_level == 1:
                recs.append("Launch basic awareness training with mandatory completion tracking.")
            elif next_level == 2:
                recs.append("Develop repeatable training schedules and role-based baseline modules.")
            elif next_level == 3:
                recs.append("Define structured training paths and measure effectiveness using quizzes/simulations.")
            elif next_level == 4:
                recs.append("Manage training as a program with continuous learning and adaptive content.")
            elif next_level == 5:
                recs.append("Optimize training through personalization, risk-based targeting, and continuous improvement cycles.")
        elif category == "culture":
            if next_level == 1:
                recs.append("Promote a non-punitive culture for reporting and encourage basic secure habits.")
            elif next_level == 2:
                recs.append("Create repeatable culture initiatives (champions program, monthly security moments).")
            elif next_level == 3:
                recs.append("Define culture metrics and incorporate security behaviors into performance feedback loops.")
            elif next_level == 4:
                recs.append("Implement structured recognition programs and peer influence initiatives.")
            elif next_level == 5:
                recs.append("Optimize culture through continuous measurement, reinforcement, and behavior-based interventions.")
        elif category == "measurement":
            if next_level == 1:
                recs.append("Start tracking basic awareness KPIs (training completion, phishing clicks, reporting rates).")
            elif next_level == 2:
                recs.append("Assess awareness on a repeatable schedule (quarterly surveys, regular phishing tests).")
            elif next_level == 3:
                recs.append("Define data analysis processes and standard dashboards for awareness outcomes.")
            elif next_level == 4:
                recs.append("Manage improvements via action plans tied to measured gaps, with owners and deadlines.")
            elif next_level == 5:
                recs.append("Optimize measurement by correlating awareness metrics with incidents and business risk.")
        else:
            recs.append(f"{cat_name}: Improve controls and processes to reach next maturity level: {next_name}")

        recs.append(f"Target Next Level: {next_level} - {next_name} (Current Score: {score})")
        return recs

    def run_assessment(self, survey_file):
        """
        Run complete SAMM assessment.

        Args:
            survey_file: Path to survey data CSV

        Returns:
            Boolean indicating success
        """
        print("Starting SAMM Assessment...")
        print("=" * 50)

        # Load survey data
        responses = self.load_survey_data(survey_file)
        if not responses:
            print("No responses found in survey file.")
            return False

        # Calculate scores for each category
        category_results = {}
        overall_weighted_score = 0.0

        for cat_key, cat_info in ASSESSMENT_CATEGORIES.items():
            score = self.calculate_category_score(responses, cat_key)
            level_num, level_name = self.assess_maturity_level(score)

            cat_recs = self.generate_recommendations(cat_key, score, level_num)

            category_results[cat_key] = {
                "name": cat_info["name"],
                "weight": cat_info["weight"],
                "score": score,
                "maturity_level": {
                    "level": level_num,
                    "name": level_name
                },
                "recommendations": cat_recs
            }

            overall_weighted_score += score * cat_info["weight"]

        overall_weighted_score = round(overall_weighted_score, 2)
        overall_level_num, overall_level_name = self.assess_maturity_level(overall_weighted_score)

        # Store results in self.results dictionary
        self.results = {
            "generated_at": __import__("datetime").datetime.now().isoformat(),
            "survey_file": survey_file,
            "response_count": len(responses),
            "overall": {
                "weighted_score": overall_weighted_score,
                "maturity_level": {
                    "level": overall_level_num,
                    "name": overall_level_name
                }
            },
            "categories": category_results
        }

        # Print summary
        print(f"Responses processed: {len(responses)}")
        print(f"Overall Weighted Score: {overall_weighted_score}")
        print(f"Overall Maturity Level: {overall_level_num} - {overall_level_name}")
        print("=" * 50)

        return True

    def save_results(self, output_file):
        """
        Save assessment results to JSON file.

        Args:
            output_file: Path to output JSON file

        Returns:
            Boolean indicating success
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 samm_engine.py <survey_csv_file>")
        sys.exit(1)

    survey_file = sys.argv[1]
    output_file = os.path.join(os.path.dirname(__file__), "..", "reports", "samm_results.json")

    # Create SAMMAssessment instance
    samm = SAMMAssessment()

    # Run assessment and save results
    ok = samm.run_assessment(survey_file)
    if not ok:
        sys.exit(1)

    if samm.save_results(output_file):
        print(f"Results saved to: {output_file}")
    else:
        sys.exit(1)
