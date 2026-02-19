# 🧠 Lab 1 — Introduction to Human Risk Assessment

## 📌 Lab Summary

This lab introduces **human risk assessment** as a cybersecurity discipline focused on understanding how user behavior, awareness, and organizational culture influence security outcomes.

A complete workflow was implemented:

- Build a human risk assessment framework
- Store assessment data in a SQLite database
- Collect responses via a web-based survey (Apache + PHP + SQLite)
- Generate sample participant data for testing
- Calculate risk scores (per category + overall)
- Produce charts and a summary report for stakeholders

---

## 🎯 Objectives

By completing this lab, I was able to:

- Understand fundamental concepts of human risk assessment in cybersecurity
- Set up a basic risk assessment framework using open-source tools
- Define and identify key risk indicators for human-centered security threats
- Create data collection instruments and store assessment data
- Analyze risk data to identify security vulnerabilities

---

## ✅ Prerequisites

- Basic cybersecurity understanding
- Linux CLI familiarity
- Basic Python programming
- Basic database concepts
- No prior risk assessment tool experience required

---

## 🧪 Lab Environment

| Component | Details |
|---|---|
| OS | Ubuntu 24.04.1 LTS |
| User | toor |
| Python | 3.12 |
| DB | SQLite3 |
| Web | Apache2 + PHP + PHP SQLite |
| Python Packages | pandas, matplotlib, seaborn, numpy |

---

## 📁 Repository Structure

```text
lab01-introduction-to-human-risk-assessment/
├── README.md
├── framework/
│   ├── risk-framework.md
│   └── risk-indicators.txt
├── data/
│   ├── assessment-data.csv
│   └── assessment.db
├── surveys/
│   └── (optional notes / future survey versions)
├── reports/
│   ├── category_scores.png
│   ├── risk_distribution.png
│   └── summary_report.md
├── scripts/
│   ├── risk_scoring.py
│   ├── risk_dashboard.py
│   ├── generate_sample_data.py
│   └── analyze_data.py
├── commands.sh
├── output.txt
├── interview_qna.md
└── troubleshooting.md
````

> Note: The web survey files are deployed under Apache at:
> `/var/www/html/risk-survey/`
>
> * `index.html`
> * `process_survey.php`

These are included as lab-created artifacts and should be tracked in the repo under a matching folder (example: `web/risk-survey/`) for GitHub.

---

## 🧩 What Was Implemented

### 1) Human Risk Framework

A structured framework was created to define:

* Risk categories (behavioral, knowledge, environmental)
* Assessment methodology (collection → analysis → reporting)
* Success metrics for improvement tracking

### 2) Key Risk Indicators (KRIs)

A KRI list was built to help detect weak areas such as:

* password reuse and weak password habits
* phishing susceptibility and reporting behavior
* social engineering weakness
* unpatched device behaviors
* training gaps and policy awareness weakness

### 3) Database for Human Risk Data

A SQLite database with normalized tables:

* `participants`
* `risk_responses`
* `risk_scores`

This enables scoring, filtering, historical tracking, and reporting.

### 4) Web Survey Collection System

Apache + PHP + SQLite3 survey:

* HTML form collects participant + risk responses
* PHP script inserts into SQLite DB
* Permissions corrected for Apache (`www-data`) access
* Tested with curl and Apache status checks

### 5) Automated Risk Scoring & Reporting

Python scoring + reporting:

* Category scoring normalized to 0–100
* Weighted overall score
* Risk level classification:

  * 80–100: Low Risk
  * 60–79: Medium Risk
  * 40–59: High Risk
  * 0–39: Critical Risk

Charts + summary report were generated into `reports/`.

---

## 📊 Results Produced

From generated sample data:

* Participants generated: **20**
* Survey responses inserted: **200**
* Risk score rows calculated: **120**

Summary insights:

* Overall average score: **64.95**
* Risk levels:

  * Medium Risk: **75%**
  * High Risk: **25%**
* Lowest scoring category trend: **social_engineering**

---

## 🧠 What I Learned

* Human risk assessment requires both **technical measurement** and **behavioral indicators**
* A lightweight SQLite schema is enough for real reporting workflows
* Web-based surveys introduce access/permission challenges in Linux environments
* Automating scoring + reporting is essential to scale security culture programs
* Risk category scoring highlights where targeted awareness interventions matter most

---

## 🔐 Why This Matters (Security Relevance)

Most breaches rely on human behavior:

* phishing clicks
* credential reuse
* weak reporting culture
* social engineering pressure tactics

This lab builds a measurable framework that supports:

* awareness program design
* risk-based training prioritization
* executive reporting
* continuous improvement cycles

---

## 🌍 Real-World Applications

* Security awareness maturity measurement
* Phishing program performance tracking
* Training effectiveness reporting (before/after)
* Department-based risk comparisons (HR vs IT vs Finance)
* Building dashboards for leadership risk visibility

---

## ✅ Final Outcome

This lab successfully delivered:

* A working **human risk assessment pipeline**
* A web survey for data intake
* SQLite storage and permission-safe access for Apache
* Automated scoring, visual reporting, and summaries
* A repeatable foundation for future advanced labs

---

## 🏁 Conclusion

Human risk assessment is a key pillar of modern cybersecurity because humans are both the most targeted and most variable part of security systems.

This lab created an end-to-end baseline system that can evolve into advanced analytics, trend tracking, and enterprise security culture measurement.
