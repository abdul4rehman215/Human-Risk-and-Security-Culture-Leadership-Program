#!/bin/bash
# Lab 13: Data-Driven Behavior Change - Commands Executed
# Environment: Ubuntu 24.04.1 LTS | User: toor

# ----------------------------
# Task 1: Project setup
# ----------------------------
mkdir -p ~/behavior-lab/{data,scripts,visualizations,web}
cd ~/behavior-lab

sudo apt update
sudo apt install -y python3-pip python3-venv nodejs npm

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn

# ----------------------------
# Task 1: Create data template
# ----------------------------
nano data/behavior_template.csv
head -n 6 data/behavior_template.csv

# ----------------------------
# Task 1: Create data generator
# ----------------------------
nano scripts/generate_data.py
chmod +x scripts/generate_data.py

# ----------------------------
# Task 2: Create analysis script
# ----------------------------
nano scripts/analyze_behavior.py
chmod +x scripts/analyze_behavior.py

# ----------------------------
# Task 2: Create visualization generator
# ----------------------------
nano scripts/create_charts.py
chmod +x scripts/create_charts.py

# ----------------------------
# Task 3: Build dashboard (HTML + JS)
# ----------------------------
nano web/dashboard.html
nano web/dashboard.js

# ----------------------------
# Task 3: Export data for web
# ----------------------------
nano scripts/export_for_web.py
chmod +x scripts/export_for_web.py

# ----------------------------
# Task 4: Pattern detection
# ----------------------------
nano scripts/detect_patterns.py
chmod +x scripts/detect_patterns.py

# ----------------------------
# Task 4: Run full workflow
# ----------------------------
cd scripts
python3 generate_data.py
python3 analyze_behavior.py
python3 create_charts.py
python3 export_for_web.py
python3 detect_patterns.py

# ----------------------------
# Start dashboard server
# ----------------------------
cd ../web
python3 -m http.server 8080
