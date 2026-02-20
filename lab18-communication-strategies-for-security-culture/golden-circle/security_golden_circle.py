#!/usr/bin/env python3
"""
Security Culture Golden Circle Communication Framework
Full Implementation
"""

import os
from datetime import datetime


class SecurityGoldenCircle:
    def __init__(self):
        self.why_statements = []
        self.how_statements = []
        self.what_statements = []

    def add_why(self, statement):
        """Add WHY statement"""
        if statement:
            self.why_statements.append(statement.strip())

    def add_how(self, statement):
        """Add HOW statement"""
        if statement:
            self.how_statements.append(statement.strip())

    def add_what(self, statement):
        """Add WHAT statement"""
        if statement:
            self.what_statements.append(statement.strip())

    def generate_executive_message(self):
        """
        Executive-focused message:
        Focus on ROI, strategic alignment, and measurable risk reduction
        """
        message = []
        message.append("EXECUTIVE SECURITY CULTURE BRIEF")
        message.append("=" * 60)
        message.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n")

        message.append("WHY THIS MATTERS (Strategic Purpose)")
        message.append("-" * 60)
        for w in self.why_statements:
            message.append(f"• {w}")

        message.append("\nHOW WE EXECUTE (Strategic Approach)")
        message.append("-" * 60)
        for h in self.how_statements:
            message.append(f"• {h}")

        message.append("\nWHAT WE DELIVER (Measurable Outcomes)")
        message.append("-" * 60)
        for w in self.what_statements:
            message.append(f"• {w}")

        message.append("\nStrategic Impact:")
        message.append("• Reduced cyber risk exposure")
        message.append("• Improved compliance posture")
        message.append("• Increased operational resilience")
        message.append("• Measurable ROI from security investments")

        return "\n".join(message)

    def generate_employee_message(self):
        """
        Employee-focused message:
        Focus on practical impact and personal relevance
        """
        message = []
        message.append("SECURITY CULTURE UPDATE")
        message.append("=" * 60)
        message.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n")

        message.append("WHY IT MATTERS TO YOU")
        message.append("-" * 60)
        for w in self.why_statements:
            message.append(f"• {w}")

        message.append("\nHOW WE MAKE IT EASY")
        message.append("-" * 60)
        for h in self.how_statements:
            message.append(f"• {h}")

        message.append("\nWHAT YOU WILL SEE")
        message.append("-" * 60)
        for w in self.what_statements:
            message.append(f"• {w}")

        message.append("\nYour Role:")
        message.append("• Stay alert to phishing attempts")
        message.append("• Report suspicious activity")
        message.append("• Complete required training on time")

        return "\n".join(message)

    def save_messages(self, exec_file, emp_file):
        os.makedirs(os.path.dirname(exec_file), exist_ok=True)

        exec_msg = self.generate_executive_message()
        emp_msg = self.generate_employee_message()

        with open(exec_file, "w") as f:
            f.write(exec_msg)

        with open(emp_file, "w") as f:
            f.write(emp_msg)

        return exec_msg, emp_msg


def main():
    gc = SecurityGoldenCircle()

    # WHY statements
    gc.add_why("Cybersecurity is essential to protect company assets and customer trust.")
    gc.add_why("Human behavior remains the primary source of security incidents.")
    gc.add_why("A strong security culture reduces financial and reputational risk.")

    # HOW statements
    gc.add_how("Deliver ongoing security awareness training programs.")
    gc.add_how("Implement phishing simulations and real-world exercises.")
    gc.add_how("Provide clear communication and reporting channels.")

    # WHAT statements
    gc.add_what("Reduced phishing click rates by 40%.")
    gc.add_what("Improved compliance scores to 92%.")
    gc.add_what("Decreased reported incidents by 30% year-over-year.")

    exec_path = "data/executive_message.txt"
    emp_path = "data/employee_message.txt"

    exec_msg, emp_msg = gc.save_messages(exec_path, emp_path)

    print("\nExecutive Message Preview:\n")
    print(exec_msg[:400] + "...\n")

    print("Employee Message Preview:\n")
    print(emp_msg[:400] + "...\n")

    print("Messages saved in data/ directory.")


if __name__ == "__main__":
    main()
