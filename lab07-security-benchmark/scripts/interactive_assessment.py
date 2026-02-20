#!/usr/bin/env python3
"""
Interactive Assessment Collection Tool
"""

import yaml
from datetime import datetime
import os


class InteractiveAssessment:
    def __init__(self, config_path: str, questions_path: str):
        """
        Initialize interactive assessment tool.
        """
        # Load configuration and questions
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        with open(questions_path, "r", encoding="utf-8") as f:
            self.questions = yaml.safe_load(f)

        self.domains = self.config.get("domains", {})

    def collect_organization_info(self) -> dict:
        """
        Collect organization information interactively.

        Returns:
            Dictionary with organization details
        """
        name = input("Organization name: ").strip()
        industry = input("Industry: ").strip()
        size = input("Organization size (e.g., 50, 200, 1000): ").strip()

        return {
            "name": name if name else "Unknown",
            "industry": industry if industry else "Unknown",
            "size": size if size else "Unknown",
            "date": datetime.now().date().isoformat(),
        }

    def conduct_domain_assessment(self, domain: str) -> list:
        """
        Conduct assessment for a single domain.

        Args:
            domain: Domain name

        Returns:
            List of response scores
        """
        domain_info = self.domains.get(domain, {})
        desc = domain_info.get("description", "")

        print("\n" + "=" * 60)
        print(f"Domain: {domain}")
        print(f"Description: {desc}")
        print("Rate each question from 1 to 5 (1=low maturity, 5=high maturity)")
        print("=" * 60)

        responses = []
        questions_list = self.questions.get(domain, [])

        for idx, q in enumerate(questions_list, start=1):
            prompt = q.get("question", f"Question {idx}")

            while True:
                ans = input(f"{idx}. {prompt} (1-5): ").strip()
                try:
                    val = int(ans)
                    if val < 1 or val > 5:
                        raise ValueError
                    responses.append(val)
                    break
                except ValueError:
                    print("Invalid input. Enter a number from 1 to 5.")

        return responses

    def save_responses(self, org_info: dict, responses: dict, output_path: str):
        """
        Save assessment responses to YAML file.

        Args:
            org_info: Organization information
            responses: Assessment responses
            output_path: Path to save file
        """
        data = {
            "organization": org_info,
            "responses": responses,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    def run_assessment(self) -> str:
        """
        Execute complete interactive assessment.

        Returns:
            Path to saved responses file
        """
        org_info = self.collect_organization_info()

        responses = {}
        for domain in self.domains.keys():
            responses[domain] = self.conduct_domain_assessment(domain)

        os.makedirs("data", exist_ok=True)

        out_file = f"data/interactive_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        self.save_responses(org_info, responses, out_file)

        print(f"\n[INFO] Responses saved to: {out_file}")
        return out_file


def main():
    tool = InteractiveAssessment(
        "config/framework.yaml",
        "data/questions.yaml"
    )
    tool.run_assessment()


if __name__ == "__main__":
    main()
