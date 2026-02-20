#!/usr/bin/env bash
# Lab 19: Executing Long-Term Security Programs
# Ubuntu Cloud Lab Environment

# ============================================================
# Task 1: Design Long-Term Security Program Strategy
# ============================================================

# Create project directory structure
mkdir -p ~/security_program/{config,data,reports,scripts}
cd ~/security_program

# Verify structure
ls -la

# Create program configuration
nano config/program_config.json

# Verify configuration file
cat config/program_config.json

# Create strategy development script
nano scripts/strategy_engine.py

# Make executable
chmod +x scripts/strategy_engine.py

# Execute strategy engine
cd scripts
python3 strategy_engine.py

# Verify generated strategy report
cat ../reports/strategy_report.json | head -30

cd ..

# ============================================================
# Task 2: Create Detailed Project Plans
# ============================================================

# Create project planner script
nano scripts/project_planner.py

# Make executable
chmod +x scripts/project_planner.py

# Run project planner
python3 scripts/project_planner.py

# Review project plan JSON
cat reports/project_plan.json | grep -A 5 "phase"

# Review generated CSV task list
head -20 data/task_list.csv

# ============================================================
# Task 3: Implement Continuous Monitoring System
# ============================================================

# Create monitoring system
nano scripts/monitoring_system.py

# Make executable
chmod +x scripts/monitoring_system.py

# Run monitoring system
python3 scripts/monitoring_system.py

# ============================================================
# Automated Reporting System
# ============================================================

# Create automated reporting script
nano scripts/automated_reporting.py

# Make executable
chmod +x scripts/automated_reporting.py

# Run automated reporting
python3 scripts/automated_reporting.py

# Verify reports directory
ls -lh reports/

# Verify charts
ls -lh reports/automated_reports/charts/

# ============================================================
# Task 4: Establish Governance Framework
# ============================================================

# Create governance framework script
nano scripts/governance_framework.py

# Make executable
chmod +x scripts/governance_framework.py

# Run governance framework
python3 scripts/governance_framework.py

# Create program documentation
nano reports/program_documentation.md

# Final verification
ls -lh reports/
ls -la data/
