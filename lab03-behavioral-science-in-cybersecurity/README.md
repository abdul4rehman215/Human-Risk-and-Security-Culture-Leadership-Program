# 🧠 Lab 3 — Behavioral Science in Cybersecurity  
## Applying the B.J. Fogg Behavior Model to Cyber Risk Prioritization

---

## 📌 Lab Overview

This lab explores how behavioral science principles — specifically the **B.J. Fogg Behavior Model (B = MAT)** — can enhance traditional cybersecurity risk assessment.

Instead of relying only on:

Impact × Likelihood

We enhance risk evaluation using:

Impact × Frequency × Behavioral Risk Factor

Where Behavioral Risk Factor is derived from:

- Motivation (M)
- Ability (A)
- Trigger (T)

This lab demonstrates how human behavioral components directly influence cybersecurity posture and risk prioritization.

---

## 🎯 Objectives

By completing this lab, I was able to:

- Implement the **B.J. Fogg Behavior Model** in Python
- Calculate behavioral likelihood scores (0–100 scale)
- Classify behavioral risk levels (Low / Medium / High)
- Develop a **risk prioritization algorithm** integrating behavioral factors
- Build a comprehensive **unit + integration testing suite**
- Design a full **organizational behavioral assessment tool**
- Generate structured JSON risk reports
- Apply behavioral science to real-world security culture analysis

---

# ✅ Prerequisites

• Basic Python programming (functions, classes, dictionaries, lists)
• Understanding of Linux command line operations
• Familiarity with cybersecurity concepts (threats, vulnerabilities, risk)
• Basic knowledge of human behavior and motivation concepts

---

## 🖥️ Lab Environment

Environment used:

- Ubuntu 24.04 (Cloud Lab)
- Python 3.12.3
- Linux Kernel 6.8.x

Verification:

```bash
python3 --version
uname -a
```

---

## 🧠 Understanding the B.J. Fogg Model

The Fogg Behavior Model states:

> **Behavior occurs when Motivation, Ability, and Trigger converge.**

Formula implemented:

```
B = M × A × T
```

Where:
- Motivation (0–10)
- Ability (0–10)
- Trigger (0–10)

Normalized to 0–1 scale before multiplication, then converted to 0–100.

---

## 📂 Repository Structure

```
lab03-behavioral-science-in-cybersecurity/
│
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│
└── scripts/
    ├── fogg_model.py
    ├── risk_prioritization.py
    ├── test_system.py
    └── org_assessment.py
```

---

## 🧪 Tasks Completed

### ✅ Task 1 — Fogg Behavior Model Implementation
- Created reusable Python class
- Behavior scoring logic
- Risk classification
- Recommendation engine
- Trend analysis
- JSON export capability

### ✅ Task 2 — Risk Prioritization Algorithm
- Combined:
  - Impact score
  - Threat frequency
  - Behavioral inverse score
- Sorted risk scenarios by calculated priority
- Generated structured text report

### ✅ Task 3 — Comprehensive Test Suite
- Unit testing for:
  - Behavior scoring
  - Risk prioritization
  - Data export
- Integration testing
- Validation of JSON output
- PASS/FAIL result reporting

### ✅ Task 4 — Organizational Assessment Tool
- Department-based profiling:
  - HR
  - Marketing
  - Finance
  - IT
  - Executives
- Realistic behavioral scoring
- Risk adjustment for high-value targets
- Generated:
  - Structured text report
  - JSON export file

---

## 📊 Key Behavioral Insights Identified

- Low ability often drives high risk more than low motivation
- Executives and Finance departments require stronger triggers
- Technical teams often need motivational reinforcement
- Behavioral risk can drastically change traditional priority scores

---

## 🏆 Expected Outcomes Achieved

✔ Functional Fogg Model implementation  
✔ Risk prioritization with behavioral weighting  
✔ Fully passing unit + integration tests  
✔ Organizational assessment engine  
✔ Valid JSON exports  
✔ Actionable security recommendations  

---

## 🌍 Real-World Applications

This behavioral risk framework can be used for:

- Security awareness program design
- Risk-based security investment decisions
- Targeted phishing simulations
- Department-level intervention strategies
- Security culture measurement
- Executive-level reporting
- Compliance and policy effectiveness analysis

---

## 📌 Conclusion

This lab bridges behavioral psychology with cybersecurity risk management.

Traditional risk model:

Impact × Likelihood

Enhanced behavioral model:

Impact × Frequency × (100 − Behavior Score)

By integrating Motivation, Ability, and Triggers, organizations can:

- Identify weakest security components
- Design targeted interventions
- Improve organizational security culture
- Allocate security resources intelligently

This approach transforms cybersecurity from purely technical control management into a human-centered strategic discipline.

---

🔐 Lab Completed Successfully  
