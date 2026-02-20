# 🔐 Lab 20: Final Security Culture Program Assessment

## 📌 Overview
This lab implements a **complete security culture assessment system** using Python.  
It generates sample datasets, analyzes maturity across multiple culture dimensions, produces **professional reports + charts**, prepares **presentation-ready summaries**, and finally packages everything into a **deliverables bundle + ZIP** for stakeholders.

Unlike day-to-day awareness metrics, this lab focuses on a **final program assessment** approach: **quantitative scoring + maturity mapping + actionable recommendations**.

---

## 🎯 Objectives
By the end of this lab, I was able to:

- Conduct a full security culture program assessment using **quantitative metrics**
- Build Python tools that **automate scoring and maturity classification**
- Generate professional assessment reports with:
  - Executive summary
  - Detailed technical report
  - Visual charts (bar + radar)
- Calculate maturity scores across **four key dimensions**
- Produce recommendations based on assessment findings
- Package all deliverables in a structured, review-ready format

---

## ✅ Prerequisites

- Basic Python knowledge (functions, data structures, file I/O)
- Understanding of security awareness + culture concepts
- Linux command-line familiarity
- Basic data analysis concepts

---

## 🧪 Lab Environment
This lab is performed in a Linux cloud environment:

- **Ubuntu 22.04 LTS**
- **Python 3.10+**
- Libraries available: `pandas`, `matplotlib`, `seaborn`, `numpy`
- Editors: `nano`, `vim`

---

## 🧠 Assessment Model Used
This lab evaluates security culture maturity using 4 categories:

| Category | What it measures | Example Inputs |
|---------|-------------------|----------------|
| **Awareness** | Training + phishing resilience | completion rate, scores, click rate |
| **Behavior** | Reporting + compliance behavior | self reporting, compliance rate |
| **Culture** | Leadership + engagement sentiment | leadership score + survey data |
| **Outcomes** | Incident response effectiveness | resolution rate, response time |

### Weighted Scoring
Each category contributes to the overall score using configured weights:

- Awareness: **0.25**
- Behavior: **0.30**
- Culture: **0.25**
- Outcomes: **0.20**

### Maturity Levels
Overall score maps into maturity stages:

- **Initial** (0–20)
- **Developing** (21–40)
- **Defined** (41–60)
- **Managed** (61–80)
- **Optimizing** (81–100)

---

## 🧩 What You Build in This Lab

### 1) Data Generation System
A generator produces realistic sample data including:

- Training metrics
- Phishing simulation results
- Incident handling metrics
- Compliance metrics
- Leadership/culture indicators
- Survey responses (1–5 scale)

### 2) Automated Assessment Analyzer
A scoring engine loads JSON datasets and calculates:

- Awareness score
- Behavior score
- Culture score
- Outcomes score
- Weighted overall score
- Maturity level label (using thresholds)
- Category-based + maturity-based recommendations

### 3) Report & Visualization Generator
Creates stakeholder-ready outputs:

- `executive_summary.txt`
- `detailed_report.txt`
- `maturity_scores.png` (bar chart)
- `maturity_radar.png` (radar chart)

### 4) Presentation Materials Generator
Creates leadership presentation assets:

- Slide outline (ready for PPT conversion)
- Speaker notes / talking points

### 5) Deliverables Packaging Utility
Packages everything into:

- A timestamped deliverables folder
- A `.zip` archive for easy distribution

---

## 📁 Repository Structure

```text
lab20-final-security-culture-program-assessment/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│ 
├── data/
│   ├── training_metrics.json
│   ├── phishing_metrics.json
│   ├── incident_metrics.json
│   ├── compliance_metrics.json
│   ├── culture_metrics.json
│   └── survey_responses.json
│
├── reports/
│   ├── assessment_results.json
│   ├── executive_summary.txt
│   ├── detailed_report.txt
│   ├── maturity_scores.png
│   ├── maturity_radar.png
│   ├── presentation_outline.txt
│   └── presentation_talking_points.txt
│
├── scripts/
│   ├── config.py
│   ├── generate_data.py
│   ├── assessment_analyzer.py
│   ├── report_generator.py
│   ├── presentation_summary.py
│   └── package_deliverables.py
│
└── deliverables/
    ├── security_culture_assessment_<timestamp>/
    └── security_culture_assessment_<timestamp>.zip
```

---

## 📦 Deliverables Produced

At completion, you will have:

* ✅ Raw datasets (`data/*.json`)
* ✅ Final assessment results (`assessment_results.json`)
* ✅ Executive and detailed reports (`.txt`)
* ✅ Charts (`.png`)
* ✅ Presentation outline + talking points
* ✅ Packaged deliverables folder + ZIP archive

---

## 📌 Why This Matters (Real-World Relevance)

Security programs often fail because organizations don’t measure culture properly.

This lab demonstrates how to:

* convert awareness signals into **maturity scores**
* track culture as a measurable program outcome
* produce **stakeholder-ready reporting**
* create repeatable quarterly assessment workflows

In real enterprises, this approach supports:

* Security governance and audit reporting
* Program ROI communication to leadership
* Benchmarking culture improvements over time
* Data-driven decision making for training and campaigns

---

## 🏁 Key Takeaways

After this lab, you should understand how to:

* translate security culture into measurable scoring models
* automate assessment workflows end-to-end
* generate professional reporting artifacts for leadership
* package evidence for audits and stakeholder review

---

## ✅ Conclusion

This lab completes the security culture lifecycle by implementing a final assessment system that is:

* automated
* quantitative
* maturity-based
* reporting-driven
* deliverables-ready

It can be reused as a quarterly/annual assessment tool for real security culture programs.
