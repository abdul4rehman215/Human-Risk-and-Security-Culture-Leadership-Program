#!/usr/bin/env python3
"""
AIDA Model Implementation for Security Training Messages
Complete implementation version
"""

import csv
import json
from datetime import datetime


class AidaMessageGenerator:
    def __init__(self):
        """Initialize AIDA message generator with templates."""
        self.message_templates = self.create_message_templates()

    def create_message_templates(self):
        """
        Create AIDA message templates for different audience segments.
        """
        templates = {
            "high_risk_executives": {
                "attention": "URGENT: Executive Security Alert - You Are a Prime Target",
                "interest": (
                    "As a senior executive, you handle sensitive information and make critical decisions. "
                    "Cybercriminals specifically target executives for their access privileges."
                ),
                "desire": (
                    "Protect your reputation and company assets by mastering advanced security practices. "
                    "Join executives who have strengthened their security posture."
                ),
                "action": "Schedule your executive security briefing within 48 hours. Contact security@company.com.",
            },
            "high_risk_it": {
                "attention": "Critical Security Update Required for IT Personnel",
                "interest": (
                    "Your technical access makes you both an asset and a potential attack vector. "
                    "Recent threats target IT professionals through sophisticated exploits."
                ),
                "desire": (
                    "Stay ahead of emerging threats with advanced technical security training tailored for IT professionals."
                ),
                "action": "Complete IT security certification within 7 days at training.company.com/it-security.",
            },

            # Added templates required by lab:
            "medium_risk_finance": {
                "attention": "Important: Finance Security Awareness Update",
                "interest": (
                    "Finance teams handle payments, invoices, and sensitive financial records. "
                    "Attackers often use phishing and fraud tactics to exploit finance workflows."
                ),
                "desire": (
                    "Strengthen your fraud detection skills and protect company funds. "
                    "You will learn practical techniques to verify payment requests and spot scams."
                ),
                "action": "Complete the finance security module within 14 days at training.company.com/finance-security.",
            },
            "low_risk_general": {
                "attention": "Security Awareness: Quick Skills for Everyday Safety",
                "interest": (
                    "Even low-risk roles can be targeted through phishing and social engineering. "
                    "Small habits can prevent major incidents."
                ),
                "desire": (
                    "Build confidence in recognizing suspicious activity and protecting your accounts. "
                    "These skills make your work safer and easier."
                ),
                "action": "Complete the general security refresher this month at training.company.com/security-awareness.",
            },
            "never_trained": {
                "attention": "Action Required: Complete Your First Security Training",
                "interest": (
                    "Our records show you have not completed security training yet. "
                    "Training ensures you understand safe practices and reporting procedures."
                ),
                "desire": (
                    "Get started quickly with a beginner-friendly course. "
                    "You will learn essential steps to protect yourself and the organization."
                ),
                "action": "Complete onboarding security training within 7 days at training.company.com/onboarding-security.",
            },
            "incident_history": {
                "attention": "Immediate Follow-Up: Security Refresher Needed",
                "interest": (
                    "Recent incidents show there is a higher chance of repeat events without reinforcement. "
                    "This refresher focuses on practical prevention and correct reporting steps."
                ),
                "desire": (
                    "Improve your security habits with targeted practice. "
                    "This will reduce future risk and increase confidence during suspicious events."
                ),
                "action": "Complete incident refresher training within 72 hours at training.company.com/incident-refresher.",
            },
        }
        return templates

    def determine_message_category(self, employee):
        """
        Determine appropriate AIDA template based on employee profile.

        Priority:
        1) incident_history (Moderate/Severe)
        2) never_trained
        3) executives high risk
        4) IT high risk
        5) finance medium risk
        6) low risk general (default)
        """
        dept = employee.get("department", "")
        risk = int(employee.get("risk_score", 0))
        last_training = employee.get("last_training", "")
        incident = employee.get("incident_history", "None")

        # Incident history first (highest priority)
        if incident in ("Moderate", "Severe"):
            return "incident_history"

        # Never trained
        if last_training == "Never":
            return "never_trained"

        # Department and risk combinations
        if dept == "Executive" and risk >= 9:
            return "high_risk_executives"

        if dept == "IT" and risk >= 8:
            return "high_risk_it"

        if dept == "Finance" and 5 <= risk <= 8:
            return "medium_risk_finance"

        # Default
        return "low_risk_general"

    def personalize_interest(self, interest_template, employee):
        """
        Add personalization to interest section based on experience.
        """
        yrs = int(employee.get("years_experience", 0))
        name = employee.get("name", "Employee")

        if yrs < 2:
            extra = f" Since you're relatively new, {name}, this training will help you build safe habits early."
        elif yrs > 10:
            extra = f" With your extensive experience, {name}, your leadership can set a strong security example for others."
        else:
            extra = f" As a key team member, {name}, you can become a security advocate by applying these steps consistently."

        return interest_template + extra

    def format_full_message(self, template, employee):
        """
        Format complete AIDA message with all components.
        """
        name = employee.get("name", "Employee")
        dept = employee.get("department", "Unknown")
        role = employee.get("role", "Unknown Role")
        risk = employee.get("risk_score", "N/A")
        location = employee.get("location", "Unknown")

        attention = template["attention"]
        interest = self.personalize_interest(template["interest"], employee)
        desire = template["desire"]
        action = template["action"]

        msg = (
            f"Hello {name},\n\n"
            f"You are receiving this message as part of our targeted security awareness program.\n"
            f"Profile context: Department={dept}, Role={role}, Location={location}, Risk Score={risk}\n\n"
            f"ATTENTION:\n{attention}\n\n"
            f"INTEREST:\n{interest}\n\n"
            f"DESIRE:\n{desire}\n\n"
            f"ACTION:\n{action}\n\n"
            "Thank you,\n"
            "Security Awareness Team\n"
        )
        return msg

    def generate_personalized_message(self, employee):
        """
        Generate personalized AIDA message for an employee.
        """
        category = self.determine_message_category(employee)
        template = self.message_templates[category]

        full_message = self.format_full_message(template, employee)

        personalized_message = {
            "employee_id": employee.get("employee_id"),
            "employee_name": employee.get("name"),
            "department": employee.get("department"),
            "role": employee.get("role"),
            "risk_score": int(employee.get("risk_score", 0)),
            "message_category": category,
            "generated_date": datetime.utcnow().isoformat() + "Z",
            "aida_components": {
                "attention": template["attention"],
                "interest": self.personalize_interest(template["interest"], employee),
                "desire": template["desire"],
                "action": template["action"],
            },
            "full_message": full_message,
        }

        return personalized_message

    def export_messages_for_delivery(self, messages, output_file):
        """
        Export messages in email-ready CSV format.

        Columns:
        employee_id, employee_name, email_subject, email_body, priority
        """

        def priority_for_category(cat: str) -> str:
            if cat in ("high_risk_executives", "high_risk_it", "incident_history"):
                return "High"
            if cat in ("never_trained", "medium_risk_finance"):
                return "Medium"
            return "Low"

        fieldnames = ["employee_id", "employee_name", "email_subject", "email_body", "priority"]

        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for m in messages:
                cat = m.get("message_category", "low_risk_general")
                subject = m.get("aida_components", {}).get("attention", "Security Training Update")
                body = m.get("full_message", "")
                writer.writerow(
                    {
                        "employee_id": m.get("employee_id"),
                        "employee_name": m.get("employee_name"),
                        "email_subject": subject,
                        "email_body": body,
                        "priority": priority_for_category(cat),
                    }
                )

    def main_generate(self, employees_csv="employees.csv"):
        """
        Convenience runner used by main().
        """
        employees = []
        with open(employees_csv, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["years_experience"] = int(row.get("years_experience", 0))
                row["risk_score"] = int(row.get("risk_score", 0))
                employees.append(row)

        messages = []
        for emp in employees:
            messages.append(self.generate_personalized_message(emp))

        # Save messages to JSON
        json_file = "aida_messages.json"
        with open(json_file, "w") as f:
            json.dump(messages, f, indent=2)

        # Export for email delivery
        delivery_csv = "messages_for_delivery.csv"
        self.export_messages_for_delivery(messages, delivery_csv)

        # Display sample messages from different categories
        print("\n=== AIDA MESSAGE GENERATION COMPLETE ===")
        print(f"Total messages generated: {len(messages)}")
        print(f"Saved JSON: {json_file}")
        print(f"Saved delivery CSV: {delivery_csv}\n")

        # Show one sample per category (up to 5)
        shown = set()
        for m in messages:
            cat = m["message_category"]
            if cat in shown:
                continue
            shown.add(cat)
            print(f"--- SAMPLE CATEGORY: {cat} ---")
            print(m["full_message"][:800])
            print("\n")
            if len(shown) >= 5:
                break

        return messages


def main():
    """Main function to generate AIDA messages."""
    gen = AidaMessageGenerator()
    gen.main_generate("employees.csv")


if __name__ == "__main__":
    main()
