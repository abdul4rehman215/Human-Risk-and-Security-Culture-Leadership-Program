#!/usr/bin/env bash
# Lab 7: Benchmarking Your Security Program (commands executed)

# Task 1: Set Up the Benchmarking Environment

sudo apt update && sudo apt install -y python3-pip python3-venv

mkdir -p ~/security-benchmark
cd ~/security-benchmark

python3 -m venv venv
source venv/bin/activate

pip install pandas pyyaml matplotlib seaborn
pip freeze > requirements.txt

mkdir -p config data scripts reports

nano config/framework.yaml
nano data/questions.yaml
nano data/sample_responses.yaml

# Task 2: Develop the Benchmarking Analysis Script

nano scripts/benchmark_analyzer.py
nano scripts/report_generator.py
nano scripts/run_benchmark.py

chmod +x scripts/*.py

# Task 3: Implement Interactive Assessment Collection

nano scripts/interactive_assessment.py

cd ~/security-benchmark
source venv/bin/activate
python3 scripts/interactive_assessment.py

# Task 4: Generate and Analyze Reports

python3 scripts/run_benchmark.py data/sample_responses.yaml
cat reports/assessment_report.md
xdg-open reports/domain_scores.png

nano scripts/compare_assessments.py
python3 scripts/compare_assessments.py data/sample_responses.yaml data/sample_responses.yaml

# Troubleshooting helper command used in lab text
python3 -c "import yaml; print(yaml.safe_load(open('data/sample_responses.yaml')))"
