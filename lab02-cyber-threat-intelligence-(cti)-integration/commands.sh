#!/usr/bin/env bash
# Lab 2: CTI Integration - Commands Executed (Ubuntu 24.04)

python3 --version
pip3 --version
libreoffice --version

mkdir -p ~/cti_lab/{data,scripts,output}
cd ~/cti_lab
ls -la

# Download feeds (follow redirects)
curl -L -o data/malware_hashes.csv "https://bazaar.abuse.ch/export/csv/recent/"
curl -L -o data/feodo_ips.csv "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
curl -L -o data/urlhaus_domains.csv "https://urlhaus.abuse.ch/downloads/csv/"

# Backup raw data
cp -r data data_backup

# Verify downloads
ls -lh data/
head -n 12 data/malware_hashes.csv
head -n 12 data/feodo_ips.csv
head -n 12 data/urlhaus_domains.csv

# Create and run CTI processing
nano ~/cti_lab/scripts/process_cti.py
cd ~/cti_lab
python3 scripts/process_cti.py

# Verify outputs
ls -lh output/
python3 -m json.tool output/master_cti_dataset.json >/dev/null && echo "JSON looks valid"

# Create spreadsheets
nano ~/cti_lab/scripts/create_spreadsheet.py
cd ~/cti_lab
python3 scripts/create_spreadsheet.py
ls -lh output/cti_main_sheet.csv output/cti_risk_summary.csv
libreoffice --calc output/cti_main_sheet.csv &
head -n 6 output/cti_main_sheet.csv

# Risk analyzer
nano ~/cti_lab/scripts/risk_analyzer.py
cd ~/cti_lab
python3 scripts/risk_analyzer.py
ls -lh output/risk_assessment_report.json
python3 -m json.tool output/risk_assessment_report.json >/dev/null && echo "Report JSON looks valid"

# Risk matrix
nano ~/cti_lab/scripts/risk_matrix.py
cd ~/cti_lab
python3 scripts/risk_matrix.py
cat output/risk_matrix.csv
libreoffice --calc output/risk_matrix.csv &

# Visualization dashboard
nano ~/cti_lab/scripts/visualize_threats.py
cd ~/cti_lab
python3 scripts/visualize_threats.py
firefox output/threat_dashboard.html &
xdg-open output/threat_dashboard.html &
ls -lh output/threat_dashboard.html
head -n 18 output/threat_dashboard.html

# Final listing
find output -maxdepth 1 -type f -printf "%f\n" | sort
