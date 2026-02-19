# 🧩 Lab 05 — Role-Based Risk Identification

## 📌 Overview
This lab implements a **role-based risk assessment** workflow using Python.  
The goal is to calculate security risk per organizational role using:
- **Role attributes** (access level, sensitivity, exposure, privileges)
- **Cyber Threat Intelligence (CTI)** threat targeting data
- **Risk classification logic** (CRITICAL / HIGH / MEDIUM / LOW / MINIMAL)
- **Reports + visualizations** for leadership and security operations

The output helps identify which roles are most likely to be targeted or abused, and where security controls should be prioritized.

---

## 🎯 Objectives
By the end of this lab, I was able to:

- Understand role-based risk assessment in organizational security contexts
- Identify security risks tied to different organizational roles
- Build a Python tool to analyze role-based risks
- Apply CTI data to modify risk scores dynamically
- Generate risk reports and classify roles by risk level

---

## 🧰 Prerequisites
- Basic Python knowledge
- Understanding of JSON format
- Familiarity with Linux CLI
- Basic organizational security concepts

---

## 🖥️ Lab Environment
- OS: Ubuntu 24.04.1 LTS  
- Python: 3.12.3  
- Virtual Environment: `risk_env`

Environment checks performed:
- `/etc/os-release`
- `python3 --version`

---

## 📁 Repo Structure (Lab Folder)
```text
lab05-role-based-risk-identification/
├── README.md
├── commands.sh
├── output.txt
├── risk_env/                       # Python virtual environment (not committed)
├── organizational_roles.json        # Role data
├── cti_data.json                   # CTI threat data
├── role_risk_analyzer.py           # Core risk scoring engine
├── run_analysis.py                 # Main workflow runner + charts + reports
├── advanced_classifier.py          # Advanced classification + risk factors + recommendations
├── filter_high_risk_roles.py       # Filter roles above a threshold
├── comprehensive_risk_report.json  # Generated report (example artifact)
├── detailed_risk_report.txt        # Generated role-by-role report
├── advanced_risk_classification.json
├── classification_summary.txt
└── risk_analysis_charts.png        # Visualization output
```

---

## ⚙️ How It Works

### ✅ Phase 1 — Data Inputs

1. `organizational_roles.json` defines roles with attributes like:

   * access_level
   * data_sensitivity
   * external_exposure
   * privilege_level

2. `cti_data.json` defines threats targeting role types such as:

   * executive
   * technical
   * management
   * support
   * sales

---

### ✅ Phase 2 — Base Risk Score

Base Score formula (0–100):

[
(access_level * 0.3 + data_sensitivity * 0.25 + external_exposure * 0.25 + privilege_level * 0.2) * 10
]

This provides a consistent baseline risk score derived from role attributes.

---

### ✅ Phase 3 — CTI Threat Modifiers

The CTI dataset adjusts risk using threat severity:

* If a role type is a target in CTI → risk increases
* Modifier logic:

  * `modifier += severity * 0.1`

Final Score = Base Score × Modifier (capped at 100)

---

### ✅ Phase 4 — Risk Classification

Score thresholds:

* **CRITICAL** ≥ 80
* **HIGH** ≥ 60
* **MEDIUM** ≥ 40
* **LOW** ≥ 20
* **MINIMAL** < 20

---

### ✅ Phase 5 — Reports & Visuals

Generated artifacts:

* `comprehensive_risk_report.json` (full structured report)
* `detailed_risk_report.txt` (human-readable breakdown)
* `risk_analysis_charts.png` (charts for stakeholder review)

Advanced classification adds:

* department multipliers
* risk factor identification
* control recommendations

---

## 📊 Results Summary (From This Run)

* Total Roles Analyzed: **5**
* Highest risk roles:

  * **Chief Executive Officer** (CRITICAL)
  * **IT Administrator** (CRITICAL)
  * **HR Manager** (CRITICAL)
* Medium risk roles:

  * Sales Representative
  * Customer Support Agent

Key observation:

* **CTI significantly increased contextual risk accuracy**
* Privileged roles + high-value roles rose to the top quickly

---

## 🔐 Why This Matters (Security Relevance)

Role-based risk identification supports:

* Least privilege and access governance
* Targeted monitoring of high-value accounts
* CTI-driven security decision making
* Better awareness training targeting (executives/support/sales)
* Stronger incident prevention for insider misuse and phishing

---

## 🌍 Real-World Applications

This approach is useful for:

* SOC triage and alert tuning (focus on CRITICAL roles)
* Identity security and IAM prioritization
* Access review programs (quarterly or monthly)
* Executive protection programs (spear phishing, impersonation)
* Audit and compliance reporting (risk-driven controls)

---

## ✅ Conclusion

This lab demonstrated a practical method to map **organizational roles to measurable security risk** using:

* Weighted attribute scoring
* CTI-based context enrichment
* Automated classification and reporting
* Advanced recommendations based on role factors

Role-based risk identification helps security teams allocate resources effectively and protect the most targeted and privileged roles first.
