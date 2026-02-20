# 🧪 Lab 7: Benchmarking Your Security Program

## 📌 Overview
This lab builds a **Security Program Maturity Benchmarking** toolkit using a weighted maturity model across key security domains (governance, risk, IR, awareness, and technical controls).  
You’ll create a benchmarking environment, define an assessment framework in YAML, run maturity scoring, and generate reports + charts.

---

## 🎯 Objectives
By the end of this lab, I was able to:

- Understand security program maturity assessment frameworks and methodologies
- Install and configure a benchmarking environment on Linux (Ubuntu 24.04)
- Analyze security program maturity using standardized metrics
- Develop Python scripts to automate security benchmarking processes
- Generate maturity reports and identify improvement opportunities

---

## ✅ Prerequisites
- Basic knowledge of cybersecurity frameworks (NIST, ISO 27001)
- Linux command-line familiarity
- Python basics (functions, loops, file I/O)
- Understanding of governance and security program concepts

---

## 🧰 Lab Environment
- OS: **Ubuntu 24.04.1 LTS**
- User: **toor**
- Tools:
  - Python 3 + pip
  - python3-venv
  - nano editor
  - pandas, pyyaml, matplotlib, seaborn

---

## 📁 Repository Structure
```text
lab07-security-benchmark/
├── README.md
├── commands.sh
├── output.txt
├── requirements.txt
├── config/
│   └── framework.yaml
├── data/
│   ├── questions.yaml
│   ├── sample_responses.yaml
│   └── interactive_responses_YYYYMMDD_HHMMSS.yaml
├── scripts/
│   ├── benchmark_analyzer.py
│   ├── report_generator.py
│   ├── run_benchmark.py
│   ├── interactive_assessment.py
│   └── compare_assessments.py
├── reports/
│   ├── assessment_report.md
│   ├── domain_scores.png
│   └── assessment_trend.png
├── interview_qna.md
└── troubleshooting.md
````

---

## 🧩 What This Lab Implements

### ✅ 1) Benchmarking Framework (YAML-driven)

You define:

* domains + weights
* maturity levels (1–5)
* thresholds for scoring bands

### ✅ 2) Question Bank + Weighted Scoring

Each domain has questions with internal weights.

### ✅ 3) Automated Scoring Engine

* calculates **domain maturity scores**
* calculates **overall weighted maturity**
* maps score → **maturity level (1–5)**

### ✅ 4) Reporting

Generates:

* Markdown report: `reports/assessment_report.md`
* Bar chart PNG: `reports/domain_scores.png`

### ✅ 5) Interactive Assessments

Collect responses interactively and saves YAML into `data/`.

### ✅ 6) Trend Comparison

Compare multiple YAML assessments and generate:

* Trend chart: `reports/assessment_trend.png`

---

## ▶️ How To Run

### 1) Setup environment

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv
mkdir -p ~/security-benchmark && cd ~/security-benchmark
python3 -m venv venv
source venv/bin/activate
pip install pandas pyyaml matplotlib seaborn
pip freeze > requirements.txt
```

### 2) Run benchmark analysis (sample)

```bash
python3 scripts/run_benchmark.py data/sample_responses.yaml
```

### 3) Run interactive assessment

```bash
python3 scripts/interactive_assessment.py
```

### 4) Compare multiple assessments

```bash
python3 scripts/compare_assessments.py data/sample_responses.yaml data/sample_responses.yaml
```

---

## 📊 Results & Key Metrics

This tool calculates:

* **Domain Scores** (0–100%)
* **Overall Weighted Score** (0–100%)
* **Maturity Level (1–5)** mapped from thresholds
* **Gap analysis** to highlight improvement priorities (lowest scoring domains)

Example computed output from sample responses:

* Overall Score: **63.9%**
* Maturity Level: **2 – Developing**
* Lowest domains: **risk_management**, **incident_response**

---

## 🔥 Why This Matters (Real-World Relevance)

Security programs often improve slowly because maturity is not measured consistently.
This lab demonstrates how organizations can:

* Benchmark progress across security domains
* Identify weak areas objectively
* Track improvements over time
* Create repeatable, evidence-driven reporting for leadership

---

## ✅ Expected Outcomes Achieved

* ✔ Functional benchmarking environment
* ✔ YAML-based maturity framework
* ✔ Automated maturity scoring scripts
* ✔ Markdown reporting + visualization
* ✔ Interactive assessment collection
* ✔ Multi-assessment trend comparison

---

## 🧠 Conclusion

This lab demonstrates how maturity models provide structured measurement of a security program using standardized and weighted metrics.
By automating scoring + reporting, organizations can improve governance and prioritization decisions while tracking maturity growth over time.

