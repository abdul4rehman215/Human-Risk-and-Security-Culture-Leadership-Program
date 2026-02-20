#!/bin/bash
# Lab 20: Final Security Culture Program Assessment
# Commands executed

mkdir -p ~/security_culture_assessment/{data,reports,scripts}
cd ~/security_culture_assessment

ls -la

nano scripts/config.py
nano scripts/generate_data.py
chmod +x scripts/generate_data.py

python3 scripts/generate_data.py

ls -l data/

nano scripts/assessment_analyzer.py
python3 scripts/assessment_analyzer.py

ls -l reports/
cat reports/assessment_results.json | head -40

nano scripts/report_generator.py
python3 scripts/report_generator.py

ls -l reports/
cat reports/executive_summary.txt
cat reports/detailed_report.txt | head -40

nano scripts/presentation_summary.py
python3 scripts/presentation_summary.py

ls -l reports/ | grep presentation

nano scripts/package_deliverables.py
python3 scripts/package_deliverables.py

ls -lh deliverables/
find deliverables -maxdepth 2 -type d
ls -l deliverables/*/reports/
