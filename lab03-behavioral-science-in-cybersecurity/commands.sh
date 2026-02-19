#!/bin/bash

# ==============================
# Lab 3 - Behavioral Science in Cybersecurity
# Commands Executed
# Environment: Ubuntu 24.04
# ==============================

# Verify environment
python3 --version
uname -a

# Create project directory
mkdir -p ~/fogg_cybersecurity_lab
cd ~/fogg_cybersecurity_lab
pwd

# Create Fogg model script
nano fogg_model.py

# Make executable
chmod +x fogg_model.py
ls -lh

# Test Fogg model
python3 fogg_model.py

# Create risk prioritization module
nano risk_prioritization.py

# Verify files
ls -lh

# Test risk prioritization system
python3 risk_prioritization.py

# Create comprehensive test suite
nano test_system.py

# Run full test suite
python3 test_system.py

# Create organizational assessment tool
nano org_assessment.py

# Run organizational assessment
python3 org_assessment.py

# Verify generated JSON report
ls -lh org_risk_report.json

# Validate JSON format
python3 -m json.tool org_risk_report.json > /dev/null && echo "JSON valid"
