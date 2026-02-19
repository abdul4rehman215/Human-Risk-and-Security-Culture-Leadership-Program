#!/usr/bin/env bash
# Lab 05: Role-Based Risk Identification
# commands.sh — command execution log (Ubuntu 24.04)

# Verify OS and Python
cat /etc/os-release
python3 --version

# Create project directory
mkdir -p ~/role_risk_lab
cd ~/role_risk_lab

# Create and activate virtual environment
python3 -m venv risk_env
source risk_env/bin/activate

# Install dependencies
pip install pandas numpy matplotlib

# Verify dependencies
python3 -c "import pandas, numpy, matplotlib; print('Dependencies OK')"

# Create data files (edited via nano)
nano organizational_roles.json
python3 -m json.tool organizational_roles.json > /dev/null

nano cti_data.json
python3 -m json.tool cti_data.json > /dev/null

# Create analyzer scripts (edited via nano)
nano role_risk_analyzer.py
nano run_analysis.py

# Make scripts executable and run analysis
chmod +x role_risk_analyzer.py
chmod +x run_analysis.py
python3 run_analysis.py

# Verify generated files
ls -lh

# Advanced classification
nano advanced_classifier.py
chmod +x advanced_classifier.py
python3 advanced_classifier.py

# Review classification outputs
cat advanced_risk_classification.json | python3 -m json.tool | head -50
cat classification_summary.txt

# Inspect risk report summary
python3 -m json.tool comprehensive_risk_report.json | head -40

# Review detailed report
less detailed_risk_report.txt

# Filter high-risk roles
nano filter_high_risk_roles.py
chmod +x filter_high_risk_roles.py
python3 filter_high_risk_roles.py

# Priority list (one-liner)
python3 -c "
import json
with open('comprehensive_risk_report.json', 'r') as f:
 data = json.load(f)

critical = [(k, v) for k, v in data['detailed_analysis'].items()
 if v['risk_level'] == 'CRITICAL']

print('CRITICAL PRIORITY ROLES:')
for role_id, info in sorted(critical, key=lambda x: x[1]['final_score'], reverse=True):
 print(f\"- {info['role_name']}: {info['final_score']} ({info['department']})\")
"
