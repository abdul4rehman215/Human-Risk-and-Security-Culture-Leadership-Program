#!/usr/bin/env bash
# Lab 12: Segmenting Audiences for Security Training
# Environment: Ubuntu 24.04.1 LTS (Cloud Lab)
# User: toor

# ---------------------------
# Task 1: Setup Lab Directory
# ---------------------------
mkdir ~/security_training_lab
cd ~/security_training_lab
python3 --version

# -----------------------------------------
# Task 1: Generate Sample Employee Dataset
# -----------------------------------------
nano employee_data_generator.py

# ---------------------------------
# Task 1: Implement Segmentation
# ---------------------------------
nano audience_segmentation.py

# -----------------------------------------
# Task 2: Implement AIDA Messaging System
# -----------------------------------------
nano aida_messaging.py

# --------------------------------------
# Task 2: Create Message Analysis Tool
# --------------------------------------
nano message_analysis.py

# --------------------------------------
# Task 3: Run Complete Workflow
# --------------------------------------

# Generate employee data
python3 employee_data_generator.py

# Run segmentation analysis (creates segment_*.csv)
python3 audience_segmentation.py

# Generate AIDA messages (creates aida_messages.json + messages_for_delivery.csv)
python3 aida_messaging.py

# Analyze message effectiveness (creates training_recommendations.csv)
python3 message_analysis.py

# --------------------------------------
# Verify Output Files
# --------------------------------------
ls -lh *.csv *.json

# --------------------------------------
# Review Sample Outputs
# --------------------------------------

# View first 10 employees
head -n 11 employees.csv

# Count employees by segment (includes headers)
wc -l segment_*.csv

# Preview delivery CSV (email-ready export)
head -n 30 messages_for_delivery.csv
