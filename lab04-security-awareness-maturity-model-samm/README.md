# 🧠 Lab 04: Security Awareness Maturity Model (SAMM)

## 📌 Overview
This lab implements a **Security Awareness Maturity Model (SAMM)** framework to assess an organization’s security awareness capability using **survey data**, **weighted maturity scoring**, **statistical analysis**, and **visual reporting**.

The project includes:
- A configurable SAMM model (levels, categories, weights, thresholds)
- Synthetic survey dataset generator (realistic correlated responses)
- Maturity assessment engine (category + overall weighted scoring)
- Statistical analysis module (descriptive + demographic + correlation)
- Automated reporting system (text + HTML dashboard with charts)

---

## 🎯 Objectives
By the end of this lab, I was able to:
- Understand and implement the **Security Awareness Maturity Model (SAMM)** framework
- Develop Python scripts to **assess organizational security awareness maturity**
- Analyze survey data using **statistical methods** to calculate maturity levels
- Generate **actionable recommendations** based on assessment results
- Create **visualization reports** for security awareness metrics

---

## ✅ Prerequisites
Before starting this lab, the following knowledge was required:
- Basic Python programming knowledge
- Understanding of cybersecurity fundamentals
- Familiarity with Linux command line operations
- Basic knowledge of data analysis concepts

---

## 🧪 Lab Environment (Ubuntu 24.04)
- OS: Ubuntu 24.04.1 LTS (Noble Numbat)
- Python: 3.12.3
- pip: 24.0
- Verified core packages: `pandas`, `numpy`, `matplotlib`

---

## 🗂️ Repository Structure
```text
lab04-security-awareness-maturity-model-samm/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
├── config/
│   └── samm_config.py
├── data/
│   └── sample_survey_data.csv
├── reports/
│   ├── samm_results.json
│   ├── analysis_results.json
│   ├── category_boxplots.png
│   ├── overall_by_department.png
│   ├── overall_by_role_level.png
│   ├── overall_score_histogram.png
│   ├── samm_report.txt
│   └── samm_report.html
└── scripts/
    ├── __init__.py
    ├── generate_sample_data.py
    ├── samm_engine.py
    ├── data_analyzer.py
    └── report_generator.py
````

---

## 🧩 SAMM Model Implemented

### 📊 Categories & Weights

* **Security Governance** (25%)
* **Security Training & Education** (30%)
* **Security Culture** (25%)
* **Measurement & Metrics** (20%)

### 🧱 Maturity Levels (0–5)

0. Non-existent
1. Initial / Ad-hoc
2. Repeatable
3. Defined
4. Managed
5. Optimizing

### 🧮 Weighted Scoring

Each category score is calculated from its subcategories, then combined into an **overall weighted maturity score**.

---

## 🧪 What Was Built & Tested

### ✅ Dataset Generation

* Generated **75 realistic survey responses**
* Correlated scoring based on:

  * organization base maturity
  * department maturity bias
  * role maturity bias
  * experience bias + controlled noise

### ✅ Maturity Assessment Engine

* Reads CSV survey data
* Calculates category maturity scores
* Determines maturity level using configured thresholds
* Produces recommendations for reaching the next maturity level
* Saves results into `reports/samm_results.json`

### ✅ Statistical Analysis & Visualization

* Descriptive stats (mean/median/std/min/max)
* Demographic breakdown (department and role level)
* Correlation matrix between SAMM categories
* Visual outputs:

  * boxplots
  * department bar chart
  * role-level bar chart
  * overall score histogram

### ✅ Comprehensive Reporting

Generated:

* `samm_report.txt` (executive + technical detail + prioritized recommendations)
* `samm_report.html` (dashboard-style HTML with embedded charts)

---

## 📌 Key Insights Observed

* **Overall maturity:** Level **3 – Defined**
* **Strongest area:** Governance
* **Weakest area:** Measurement & Metrics
* **Moderate correlation:** Training ↔ Culture
* IT and Finance generally scored higher than Marketing and Operations
* Clear demographic trends by role and department

---

## ✅ Result

✔ Functional SAMM assessment framework
✔ Generated realistic dataset (75 responses)
✔ Weighted maturity score computed (0–5 scale)
✔ Statistical analysis + correlation insights completed
✔ Charts generated successfully
✔ Text + HTML reports produced for stakeholders

---

## 🌍 Why This Matters

Security awareness isn’t just training — it’s a measurable organizational capability.
A maturity model like SAMM helps organizations:

* identify awareness strengths and gaps
* prioritize improvements by risk and maturity stage
* track progress over time using repeatable measurement
* align awareness investments with business objectives

---

## 🧠 What I Learned

* How maturity models structure improvement in measurable stages
* How weighted scoring changes overall conclusions responsibly
* Why correlation and demographic analysis matter for leadership decisions
* How visualization makes security awareness data actionable
* How to automate executive reporting from raw survey data

---

## 🏢 Real-World Applications

* Enterprise security awareness benchmarking
* Annual/quarterly security culture reporting
* Risk-based improvements targeting weak categories
* Department-level awareness gap analysis
* Measuring awareness program ROI and progress over time

---

## 🏁 Conclusion

This lab provided hands-on experience implementing a complete **SAMM security awareness maturity assessment pipeline**:

* configuration → dataset → assessment → analytics → visualization → reporting

A structured model like SAMM enables organizations to move from “training done” to **measured maturity and continuous improvement**.
