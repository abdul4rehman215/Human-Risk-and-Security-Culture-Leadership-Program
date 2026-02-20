#!/usr/bin/env python3
"""
Security Culture Email Templates for Different Audiences
Full Implementation
Golden Circle aligned: WHY / HOW / WHAT
"""

from datetime import datetime
import os


class SecurityEmailTemplates:
    def __init__(self):
        self.templates = {
            "executive": {},
            "manager": {},
            "employee": {}
        }
        self.create_templates()

    def create_templates(self):
        """
        Create HTML email templates for each audience type.
        Each template follows Golden Circle structure.
        """

        # Executive Template
        self.templates["executive"] = {
            "subject": "Security Culture ROI Report - {month}",
            "body": """
<html>
<body style="font-family: Arial, sans-serif;">
  <h2>Executive Security Update</h2>

  <div style="background-color: #f0f0f0; padding: 15px; margin: 10px 0;">
    <h3>WHY This Matters</h3>
    <ul>
      <li>Risk Reduction: {risk_reduction}%</li>
      <li>Cost Savings: ${cost_savings}</li>
      <li>Compliance Score: {compliance_score}%</li>
    </ul>
  </div>

  <div style="background-color: #e8f4ff; padding: 15px; margin: 10px 0;">
    <h3>HOW We Deliver</h3>
    <ul>
      <li>Executive-aligned security culture program governance</li>
      <li>Monthly metrics review with corrective action plans</li>
      <li>Targeted improvements by department risk profile</li>
    </ul>
  </div>

  <div style="background-color: #eaffea; padding: 15px; margin: 10px 0;">
    <h3>WHAT We Achieved</h3>
    <ul>
      <li>Phishing click rate: {phishing_click_rate}%</li>
      <li>Incident reduction (monthly): {incident_reduction}%</li>
      <li>Training completion: {training_completion}%</li>
    </ul>
  </div>

  <p><b>Security Team</b><br/>Generated: {generated_date}</p>
</body>
</html>
"""
        }

        # Manager Template
        self.templates["manager"] = {
            "subject": "Manager Security Toolkit - {month}",
            "body": """
<html>
<body style="font-family: Arial, sans-serif;">
  <h2>Security Culture Manager Update</h2>

  <h3>WHY This Matters</h3>
  <p>Your team is a key line of defense against cyber threats.</p>

  <h3>HOW You Can Help</h3>
  <ul>
    <li>Encourage timely training completion</li>
    <li>Reinforce phishing reporting behaviors</li>
    <li>Use security reminders in meetings</li>
  </ul>

  <h3>WHAT To Do This Month</h3>
  <ul>
    <li>Training completion target: {team_training_target}%</li>
    <li>Current completion: {training_completion}%</li>
    <li>Reported suspicious emails: {reports_count}</li>
  </ul>

  <p><b>Security Team</b><br/>Generated: {generated_date}</p>
</body>
</html>
"""
        }

        # Employee Template
        self.templates["employee"] = {
            "subject": "Security Tip of the Week - {month}",
            "body": """
<html>
<body style="font-family: Arial, sans-serif;">
  <h2>Security Tip of the Week</h2>

  <h3>WHY It Matters</h3>
  <p>Your actions help protect the organization from cyber threats.</p>

  <h3>HOW To Stay Safe</h3>
  <ul>
    <li>Pause before clicking links</li>
    <li>Verify unexpected requests</li>
    <li>Enable multi-factor authentication</li>
  </ul>

  <h3>WHAT To Do Now</h3>
  <ul>
    <li>Complete training module: {training_module}</li>
    <li>Review checklist: {checklist_link}</li>
  </ul>

  <p><b>Security Team</b><br/>Generated: {generated_date}</p>
</body>
</html>
"""
        }

    def generate_email(self, audience_type, **kwargs):
        if audience_type not in self.templates:
            raise ValueError(f"Unknown audience type: {audience_type}")

        template = self.templates[audience_type]
        subject = template["subject"].format(**kwargs)
        body = template["body"].format(**kwargs)
        return subject, body

    def save_sample_emails(self):
        os.makedirs("templates", exist_ok=True)

        generated_date = datetime.now().strftime("%Y-%m-%d")

        samples = {
            "executive": dict(
                month="January 2026",
                risk_reduction=35,
                cost_savings="150000",
                compliance_score=92,
                phishing_click_rate=6.5,
                incident_reduction=25,
                training_completion=94,
                generated_date=generated_date
            ),
            "manager": dict(
                month="January 2026",
                team_training_target=95,
                training_completion=91,
                reports_count=18,
                generated_date=generated_date
            ),
            "employee": dict(
                month="January 2026",
                training_module="Phishing Awareness Basics",
                checklist_link="intranet.company.local/security-checklist",
                generated_date=generated_date
            )
        }

        for audience, data in samples.items():
            subject, body = self.generate_email(audience, **data)
            out_file = f"templates/sample_{audience}.html"
            with open(out_file, "w") as f:
                f.write(body)

        return True


def main():
    templates = SecurityEmailTemplates()
    templates.save_sample_emails()
    print("Sample emails created in templates/ directory:")
    print(" - templates/sample_executive.html")
    print(" - templates/sample_manager.html")
    print(" - templates/sample_employee.html")


if __name__ == "__main__":
    main()
