#!/usr/bin/env bash
# Lab 6: Building Strategic Risk Plans (Ubuntu 24.04)

# Task 1: Build a Risk-Behavior-Culture Alignment Framework
mkdir -p ~/risk_management_lab
cd ~/risk_management_lab

pip3 install pandas matplotlib seaborn numpy

# Create and test the framework module
chmod +x risk_framework.py
python3 risk_framework.py

# Verify output files
ls -lh

# Create visualization module and run
python3 risk_visualization.py

# Verify generated PNGs
ls *.png

# Task 2: Implement Role-Based Risk Assessment
chmod +x role_risk_assessment.py
python3 role_risk_assessment.py

# Task 2: Role-Based Visualizations
python3 role_visualization.py
ls *.png

# Task 3: Build Comprehensive Risk Management Reports
python3 risk_report_generator.py

# Task 3: Review and Validate Results
ls -lh *.csv *.json *.png *.md
cat risk_report.md | head -30

python3 -c "import pandas as pd; df = pd.read_csv('role_based_risk_assessment.csv'); print(df.describe())"
