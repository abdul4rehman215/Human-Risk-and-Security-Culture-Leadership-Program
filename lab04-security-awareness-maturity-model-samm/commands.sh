#!/bin/bash
# Lab 04 - Security Awareness Maturity Model (SAMM)
# Commands Executed During Lab (sequential, no explanations)

# ------------------------------
# Environment Verification
# ------------------------------
cat /etc/os-release
python3 --version
pip3 --version
python3 -c "import pandas, numpy, matplotlib; print('Core packages OK')"

# ------------------------------
# Task 1: Set Up SAMM Framework Structure
# ------------------------------
mkdir -p ~/samm-lab/{data,scripts,reports,config}
cd ~/samm-lab
touch scripts/__init__.py
tree -L 1

nano config/samm_config.py
ls config

# ------------------------------
# Step 3: Generate Sample Survey Data
# ------------------------------
nano scripts/generate_sample_data.py
cd scripts
python3 generate_sample_data.py
ls -lh ../data/
head -n 5 ../data/sample_survey_data.csv

# ------------------------------
# Task 2: Implement SAMM Assessment Engine
# ------------------------------
nano samm_engine.py
python3 samm_engine.py ../data/sample_survey_data.csv
ls -lh ../reports/
cat ../reports/samm_results.json | head -n 30

# ------------------------------
# Task 3: Develop Data Analysis Module
# ------------------------------
nano data_analyzer.py
pip3 install pandas numpy matplotlib seaborn scipy scikit-learn
python3 data_analyzer.py ../data/sample_survey_data.csv ../reports
ls -lh ../reports/

# ------------------------------
# Task 4: Create Comprehensive Reporting System
# ------------------------------
nano report_generator.py
python3 report_generator.py ../reports/samm_results.json ../reports/analysis_results.json
cat ../reports/samm_report.txt | head -n 40
xdg-open ../reports/samm_report.html &
