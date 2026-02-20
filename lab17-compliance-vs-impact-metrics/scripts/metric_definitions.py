#!/usr/bin/env python3
"""
Metric Definitions Module
Define compliance and impact metrics
"""


class MetricDefinitions:
    def __init__(self):
        self.compliance_metrics = {
            "definition": "Measures adherence to policies and training requirements",
            "examples": [
                "Training completion rates",
                "Policy acknowledgment percentages",
                "Phishing simulation click rates",
                "Assessment scores",
            ],
        }

        self.impact_metrics = {
            "definition": "Measures behavioral change and culture improvement",
            "examples": [
                "Voluntary incident reporting increases",
                "Proactive security behaviors",
                "Peer-to-peer coaching instances",
                "Security-conscious decision making",
            ],
        }

    def display_comparison(self):
        """
        Display comparison between metric types

        Print formatted comparison of both metric types
        Include definitions and examples
        Highlight key differences
        """
        print("\n" + "=" * 72)
        print("COMPLIANCE METRICS vs IMPACT METRICS (SECURITY CULTURE PROGRAMS)")
        print("=" * 72)

        print("\nCOMPLIANCE METRICS")
        print("-" * 72)
        print(f"Definition: {self.compliance_metrics['definition']}")
        print("Examples:")
        for ex in self.compliance_metrics["examples"]:
            print(f"  - {ex}")

        print("\nIMPACT METRICS")
        print("-" * 72)
        print(f"Definition: {self.impact_metrics['definition']}")
        print("Examples:")
        for ex in self.impact_metrics["examples"]:
            print(f"  - {ex}")

        print("\nKEY DIFFERENCES")
        print("-" * 72)
        print("1) What it measures:")
        print("   - Compliance: Completion / adherence (what people DID).")
        print("   - Impact: Behavior + culture change (how people CHANGED).")
        print("2) How it is used:")
        print("   - Compliance: Proves obligations were met (audits, governance).")
        print("   - Impact: Proves risk reduced and culture improved (strategy, ROI).")
        print("3) Risk interpretation:")
        print("   - High compliance can still produce low impact.")
        print("   - High impact usually requires some compliance but goes beyond it.")
        print("=" * 72 + "\n")


if __name__ == "__main__":
    metrics = MetricDefinitions()
    metrics.display_comparison()
