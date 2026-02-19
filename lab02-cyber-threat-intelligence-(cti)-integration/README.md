# 🧠 Lab 2: Cyber Threat Intelligence (CTI) Integration

This lab demonstrates how to **collect**, **normalize**, and **analyze** open-source Cyber Threat Intelligence (CTI) feeds, then generate **risk scoring**, **prioritization**, **reporting**, and a simple **visual dashboard**. It also highlights how CTI can reveal **human-driven threats** (phishing, credential theft, social engineering themes).

---

## 🎯 Objectives

By the end of this lab, I was able to:

- Integrate open-source CTI data into structured formats for analysis
- Analyze and prioritize security risks based on threat intelligence indicators
- Create risk assessment frameworks using Python
- Apply CTI data to identify human-driven security threats
- Generate actionable security recommendations from threat intelligence

---

## ✅ Prerequisites

- Basic understanding of cybersecurity concepts and common threats
- Familiarity with Linux command line operations
- Elementary Python programming knowledge
- Understanding of CSV/JSON data formats

---

## 🧪 Lab Environment

- OS: Ubuntu 24.04 (cloud machine)
- Tools: Python 3, pip, LibreOffice, curl
- CTI Feeds:
  - MalwareBazaar (recent malware hashes)
  - Feodo Tracker (malicious IP blocklist)
  - URLhaus (malicious URLs/domains)
 
---

## 📁 Repository Structure

```text
lab02-cyber-threat-intelligence-(cti)-integration/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
├── data/
│   ├── malware_hashes.csv
│   ├── feodo_ips.csv
│   ├── urlhaus_domains.csv
│   └── (optional) data_backup/   # backup copy of feeds
├── scripts/
│   ├── process_cti.py
│   ├── create_spreadsheet.py
│   ├── risk_analyzer.py
│   ├── risk_matrix.py
│   └── visualize_threats.py
└── output/
    ├── master_cti_dataset.csv
    ├── master_cti_dataset.json
    ├── cti_main_sheet.csv
    ├── cti_risk_summary.csv
    ├── risk_assessment_report.json
    ├── risk_matrix.csv
    └── threat_dashboard.html
````

---

## 🧩 What I Built

### 1) CTI Collection

Downloaded multiple public CTI feeds using `curl -L` (redirect-safe), then stored raw datasets under `data/`.

### 2) Normalization + Master Dataset

Processed each feed into a consistent structure and exported:

* `output/master_cti_dataset.json`
* `output/master_cti_dataset.csv`

### 3) Spreadsheet Outputs (LibreOffice-ready)

Generated analysis-friendly CSVs:

* `output/cti_main_sheet.csv`
* `output/cti_risk_summary.csv`

### 4) Risk Analysis + Human-Focused Threat Detection

Generated:

* Threat landscape statistics (levels, types, sources)
* Priority scoring and response timelines
* “Human-targeting” indicators (social engineering keyword signals)

Outputs:

* `output/risk_assessment_report.json`

### 5) Prioritization Matrix

Created a matrix output:

* `output/risk_matrix.csv`

> Note: This version categorizes the **Top 10 threats** from the report, matching the provided lab flow.

### 6) Visualization Dashboard (HTML)

Created a lightweight HTML dashboard:

* `output/threat_dashboard.html`

---

## ✅ Final Outcomes

After completing this lab, I had:

* A master dataset with **150 indicators** (50 per CTI source)
* Risk scoring logic and prioritization output
* Actionable recommendations for security response
* Spreadsheet outputs for management/business workflows
* A simple HTML dashboard to visualize the threat landscape

---

## 🌍 Real-World Relevance

CTI Integration is used daily in real SOC workflows:

* Blocking malicious IPs/domains at firewall/proxy/DNS
* Updating EDR/AV blocklists (hashes / indicators)
* Correlating CTI with SIEM logs (auth logs, proxy logs, endpoint telemetry)
* Identifying phishing themes and improving security awareness programs

---

## 🏁 Conclusion

This lab built a practical CTI ingestion and analysis pipeline using open sources and Python. You learned how to convert raw feeds into structured data, apply scoring, detect user-focused attack patterns, and produce outputs (reports, spreadsheets, dashboards) that support real-world security decision-making.
