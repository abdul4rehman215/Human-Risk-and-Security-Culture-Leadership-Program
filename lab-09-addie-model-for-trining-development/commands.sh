#!/usr/bin/env bash
# Lab 09: ADDIE Model for Training Development
# Environment: Ubuntu 24.04 (Cloud Lab Environment)
# User: toor

mkdir -p ~/addie_training_lab/{analyze,design,develop,implement,evaluate,scripts,data,reports}
cd ~/addie_training_lab

ls

nano scripts/addie_framework.py
chmod +x scripts/addie_framework.py
./scripts/addie_framework.py

nano scripts/analyze_phase.py
nano scripts/sample_analysis_data.py
chmod +x scripts/analyze_phase.py scripts/sample_analysis_data.py
./scripts/sample_analysis_data.py
ls -lh data/

nano scripts/design_phase.py
chmod +x scripts/design_phase.py
./scripts/design_phase.py
ls -lh design/

nano scripts/develop_phase.py
chmod +x scripts/develop_phase.py
./scripts/develop_phase.py
ls -lh develop/

nano scripts/implement_phase.py
chmod +x scripts/implement_phase.py

nano scripts/evaluate_phase.py
chmod +x scripts/evaluate_phase.py

nano scripts/complete_addie_workflow.py
chmod +x scripts/complete_addie_workflow.py
./scripts/complete_addie_workflow.py

find . -maxdepth 2 -type f | sort
