# 🧭 Lab 6: Building Strategic Risk Plans

> Designd and implemented a **strategic risk management framework** that connects **cybersecurity risks** with **human behavior** and **organizational culture**, then built **role-based prioritization**, **visualizations**, and **executive-ready reports**.

---

## 🎯 Objectives

By the end of this lab, I was able to:

- Design a strategic risk management framework aligning **risk + behavior + culture**
- Implement **role-based risk assessments** using Python
- Create prioritization matrices for risk management decisions
- Develop automated tools for **risk analysis** and **visualization**
- Build data-driven risk management plans for organizational contexts

---

## ✅ Prerequisites

- Python basics (functions, dictionaries, loops, file I/O)
- Cybersecurity risk fundamentals
- Linux command line familiarity
- Understanding of organizational roles and security responsibilities

---

## 🧪 Lab Environment

- **OS:** Ubuntu 24.04.1 LTS  
- **Python:** 3.12.3  
- **Tools/Libraries:** pandas, matplotlib, seaborn, numpy

---

## 📁 Repository Structure

```text
lab06-building-strategic-risk-plans/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│   
├── scripts/
│   ├── risk_framework.py
│   ├── risk_visualization.py
│   ├── role_risk_assessment.py
│   ├── role_visualization.py
│   ├── risk_report_generator.py
│
├── reports/
│   risk_alignment_matrix.csv
│   ├── risk_framework_data.json
│   ├── organizational_roles.json
│   ├── role_based_risk_assessment.csv
│   ├── prioritized_action_plan.json
│   ├── risk_management_report.json
│   ├── risk_report.md
│
├── visual_reports/
│   ├── risk_heatmap.png
│   ├── alignment_distribution.png
│   ├── culture_impact_chart.png
│   ├── role_risk_heatmap.png
│   ├── priority_distribution.png
│   └── action_timeline.png
````

---

## 🧠 What This Lab Builds

### 1) Risk–Behavior–Culture Alignment Framework

A scoring model that computes risk using:

* **Base severity** (critical/high/medium/low)
* **Behavior multipliers** (awareness + compliance)
* **Culture multiplier** (culture maturity reduces risk)

Outputs:

* `risk_alignment_matrix.csv`
* `risk_framework_data.json`

---

### 2) Role-Based Risk Assessment + Prioritization

A role-risk scoring engine that:

* Applies **role weights**
* Highlights **primary risks**
* Produces priority levels: **critical / high / medium / low**
* Generates a prioritized mitigation plan with timelines

Outputs:

* `role_based_risk_assessment.csv`
* `prioritized_action_plan.json`
* `organizational_roles.json`

---

### 3) Visual Risk Intelligence (Charts)

Two visualization modules generate:

* Alignment and culture influence visuals
* Role vs risk heatmaps
* Priority distribution charts
* Action plan timeline scatter plot

Outputs (PNG):

* `risk_heatmap.png`
* `alignment_distribution.png`
* `culture_impact_chart.png`
* `role_risk_heatmap.png`
* `priority_distribution.png`
* `action_timeline.png`

---

### 4) Executive Reporting (JSON + Markdown)

A report generator that consolidates:

* Executive summary (top risks + vulnerable roles)
* Detailed findings (alignment + role risk)
* Recommendations and resourcing estimates

Outputs:

* `risk_management_report.json`
* `risk_report.md`

---

## 🚀 How to Run

> Full command history is in `commands.sh`

High level execution order:

1. Generate framework matrix + config:

```bash
python3 risk_framework.py
```

2. Create alignment visualizations:

```bash
python3 risk_visualization.py
```

3. Create role-based assessment + action plan:

```bash
python3 role_risk_assessment.py
```

4. Create role-based visualizations:

```bash
python3 role_visualization.py
```

5. Generate full executive reports:

```bash
python3 risk_report_generator.py
```

---

## 📌 Results Summary

* Alignment matrix generated: **60 scenarios**
* Role-risk matrix generated: **20 combinations**
* Priority distribution (sample):

  * critical: 6
  * high: 9
  * medium: 4
  * low: 1
* Outputs include **CSV + JSON + Markdown + PNG charts**

---

## ✅ What I Learned

* Strategic risk management improves when **technical risk** is integrated with **human behavior** and **culture**
* Role-based weighting increases accuracy and supports targeted mitigation
* Visualizations make risk insights **digestible for leadership**
* Automated reporting ensures repeatability, governance readiness, and stakeholder alignment

---

## 🌍 Why This Matters (Real-World Relevance)

Organizations don’t fail only because of technical gaps—many incidents happen because:

* People click, share, reuse passwords, or bypass controls
* Culture discourages reporting or learning
* Leaders don’t prioritize security consistently

This framework enables:

* **Risk-driven security planning**
* **Actionable roadmaps**
* **Executive-ready reporting**
* **Prioritization aligned to business impact**

---

## ✅ Conclusion

This lab delivered a complete strategic risk planning toolkit:

* Risk-behavior-culture scoring model
* Role-based prioritization engine
* Automated visualization suite
* Executive reporting pipeline

It mirrors real enterprise risk workflows and can be extended with:

* More roles, departments, and risks
* Real survey data ingestion
* CTI integration
* Trend tracking over time
