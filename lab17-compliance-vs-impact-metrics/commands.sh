#!/usr/bin/env bash
# Lab 17: Compliance vs. Impact Metrics (Ubuntu 24.04)
# Commands Executed (as performed in the lab)

mkdir -p ~/metrics_lab
cd ~/metrics_lab

# (Optional) Verify Python
python3 --version

# Create metric definitions module
nano metric_definitions.py
chmod +x metric_definitions.py
python3 metric_definitions.py

# Create sample data generator
nano data_generator.py
chmod +x data_generator.py
python3 data_generator.py

# Verify CSV outputs
ls -lh *.csv

# Create compliance analyzer + visualizer
nano compliance_analyzer.py
chmod +x compliance_analyzer.py

nano compliance_visualizer.py
chmod +x compliance_visualizer.py

# Run compliance analysis + visualizations
python3 compliance_analyzer.py
python3 compliance_visualizer.py

# Create impact analyzer + visualizer
nano impact_analyzer.py
chmod +x impact_analyzer.py

nano impact_visualizer.py
chmod +x impact_visualizer.py

# Run impact analysis + visualizations
python3 impact_analyzer.py
python3 impact_visualizer.py

# Create integrated dashboard/comparison script
nano integrated_dashboard.py
chmod +x integrated_dashboard.py

# Run integrated comparison + executive dashboard + recommendations
python3 integrated_dashboard.py

# Final verification of generated artifacts
ls -lh *.png
ls -lh *.txt
