#!/usr/bin/env bash
# Lab 18: Communication Strategies for Security Culture
# Commands executed 

# -------------------------------
# Task 1 — Implementing the Golden Circle Framework
# -------------------------------

mkdir -p ~/security-communication-lab/{golden-circle,templates,scripts,logs,data}
cd ~/security-communication-lab

tree -d

nano golden-circle/security_golden_circle.py
chmod +x golden-circle/security_golden_circle.py
python3 golden-circle/security_golden_circle.py

ls -la data/

nano templates/communication_plan.py
python3 templates/communication_plan.py

ls -la data/

# -------------------------------
# Task 2 — Automated Email Communication System
# -------------------------------

nano scripts/email_config.py
chmod +x scripts/email_config.py
python3 scripts/email_config.py

ls -la data/
ls -la logs/

nano scripts/email_templates.py
chmod +x scripts/email_templates.py
python3 scripts/email_templates.py

ls -la templates/

nano scripts/email_scheduler.py
chmod +x scripts/email_scheduler.py
cd scripts
python3 email_scheduler.py
cd ..

ls -la data/
ls -la logs/

# -------------------------------
# Task 3 — Communication Dashboard
# -------------------------------

nano scripts/communication_metrics.py
chmod +x scripts/communication_metrics.py
python3 scripts/communication_metrics.py

nano scripts/communication_dashboard.py
chmod +x scripts/communication_dashboard.py
python3 scripts/communication_dashboard.py

# -------------------------------
# Final Verification
# -------------------------------

ls -la data/
ls -la logs/
ls -la templates/
