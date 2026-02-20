#!/usr/bin/env python3
"""
Email Configuration and Sender for Security Communications
Full Implementation (Simulated send for lab environment)
"""

import json
import os
from datetime import datetime


class EmailConfig:
    def __init__(self, config_file="data/email_config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
        Load email configuration from file or create default
        Returns: Dictionary with email configuration
        """
        default_config = {
            "smtp_server": "localhost",
            "smtp_port": 587,
            "from_name": "Security Team",
            "from_email": "security-team@company.local"
        }

        # If file doesn't exist, create it with defaults
        if not os.path.exists(self.config_file):
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=2)
            return default_config

        # Load existing config and merge with defaults
        try:
            with open(self.config_file, "r") as f:
                loaded = json.load(f)

            merged = default_config.copy()
            if isinstance(loaded, dict):
                merged.update(loaded)

            return merged

        except (json.JSONDecodeError, OSError):
            # If config is corrupted, rewrite defaults
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def save_config(self):
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)


class SecurityEmailSender:
    def __init__(self, config):
        self.config = config
        self.sent_log = []

    def create_message(self, to_email, subject, body):
        """
        Create email message structure
        Returns message dict
        """
        msg = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "smtp_server": self.config.get("smtp_server"),
            "smtp_port": self.config.get("smtp_port"),
            "from_name": self.config.get("from_name"),
            "from_email": self.config.get("from_email"),
            "to_email": to_email,
            "subject": subject,
            "body": body
        }
        return msg

    def send_email(self, to_email, subject, body):
        """
        Send email (simulated for lab environment)
        """
        msg = self.create_message(to_email, subject, body)

        # Simulate sending by printing
        print("\n" + "=" * 70)
        print("SIMULATED EMAIL SEND")
        print("=" * 70)
        print(f"From: {msg['from_name']} <{msg['from_email']}>")
        print(f"To: {msg['to_email']}")
        print(f"Subject: {msg['subject']}")
        print("-" * 70)

        snippet = body.strip().replace("\n", " ")
        print(snippet[:250] + ("..." if len(snippet) > 250 else ""))
        print("=" * 70)

        self.sent_log.append(msg)
        return True

    def save_log(self, filename="logs/email_log.json"):
        """
        Save email sending log to file
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.sent_log, f, indent=2)


def main():
    cfg = EmailConfig()
    sender = SecurityEmailSender(cfg.config)

    recipients = [
        "ceo@company.local",
        "manager1@company.local",
        "employee1@company.local"
    ]

    subject = "Test Security Communication"
    body = "This is a simulated test email from the security communication system."

    for r in recipients:
        sender.send_email(r, subject, body)

    sender.save_log("logs/email_log.json")
    print("\nSaved email log to logs/email_log.json")


if __name__ == "__main__":
    main()
