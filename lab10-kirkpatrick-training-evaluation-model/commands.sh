#!/usr/bin/env bash
# Lab 10: Kirkpatrick's Four-Level Training Evaluation Model
# Environment: Ubuntu 24.04 | User: toor

# -------------------------------
# Task 1: Environment Setup
# -------------------------------

mkdir -p ~/kirkpatrick_lab/{data,scripts,reports,visualizations}
cd ~/kirkpatrick_lab

ls

python3 -m venv venv
source venv/bin/activate

pip install pandas numpy matplotlib seaborn scipy

# -------------------------------
# Task 1: Data Preparation
# -------------------------------

nano data/training_data.csv
head data/training_data.csv

nano data/criteria.json
cat data/criteria.json

# -------------------------------
# Task 2: Create Core Evaluation Scripts
# -------------------------------

nano scripts/kirkpatrick_evaluator.py
nano scripts/department_analysis.py

chmod +x scripts/kirkpatrick_evaluator.py
chmod +x scripts/department_analysis.py

# -------------------------------
# Task 3: Statistical + ROI Helpers
# -------------------------------

nano scripts/statistics_helper.py
chmod +x scripts/statistics_helper.py

nano scripts/roi_calculator.py
chmod +x scripts/roi_calculator.py

# -------------------------------
# Task 4: Execute Evaluation + Analysis
# -------------------------------

cd ~/kirkpatrick_lab
source venv/bin/activate

python3 scripts/kirkpatrick_evaluator.py

python3 scripts/department_analysis.py

# -------------------------------
# Task 4: Custom Analysis
# -------------------------------

nano scripts/custom_analysis.py
chmod +x scripts/custom_analysis.py

python3 scripts/custom_analysis.py

# -------------------------------
# Final Verification
# -------------------------------

tree -L 2
