# 🧠 Lab 03: Behavioral Science in Cybersecurity (B.J. Fogg Model)

## 📌 Lab Summary
This lab applies **behavioral science** to cybersecurity by implementing the **B.J. Fogg Behavior Model**:

> **B = MAT** → Behavior occurs when **Motivation**, **Ability**, and **Trigger** converge.

Using Python, we built:
- A behavior scoring engine for cybersecurity behaviors
- A risk prioritization system that blends **traditional risk** with **behavioral risk**
- A full testing suite (unit + integration)
- An organizational assessment tool that generates actionable recommendations and exports reports

---

## 🎯 Objectives
By the end of this lab, I was able to:
- Apply the **Fogg Model (Motivation, Ability, Trigger)** to cybersecurity contexts
- Implement behavioral assessment algorithms in Python
- Develop risk prioritization systems incorporating behavioral principles
- Analyze security behaviors and generate actionable recommendations
- Create tools that support improving organizational security culture

---

## ✅ Prerequisites
- Basic Python programming (functions, classes, dictionaries, lists)
- Linux command-line familiarity
- Cybersecurity fundamentals (threats, vulnerabilities, risk)
- Basic knowledge of motivation/behavior concepts

---

## 🧪 Lab Environment
| Component | Details |
|---|---|
| OS | Ubuntu 24.04 (Cloud Lab) |
| Kernel | Linux 6.8.0-31-generic x86_64 |
| Python | Python 3.12.3 |
| User | `toor` |

---

## 🗂️ Repository Structure
```text
lab03-behavioral-science-in-cybersecurity/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
├── scripts/
│   ├── fogg_model.py
│   ├── risk_prioritization.py
│   ├── test_system.py
│   └── org_assessment.py
└── reports/
    ├── fogg_export_test.json
    ├── prioritized_export_test.json
    ├── integration_prioritized_risks.json
    └── org_risk_report.json
````

---

## 🧩 What Was Built

### 1) 🧠 Fogg Behavior Model Engine (`fogg_model.py`)

Implemented:

* Behavior score calculation using:
  **(Motivation × Ability × Trigger) × 100**
* Risk levels based on behavior likelihood:

  * **High likelihood → Low risk**
  * **Medium likelihood → Medium risk**
  * **Low likelihood → High risk**
* Automated recommendations based on weak components (M/A/T)
* Trend analysis and JSON export

---

### 2) ⚖️ Behavioral Risk Prioritization (`risk_prioritization.py`)

Implemented a scoring system that combines:

* **Business Impact (1–10)**
* **Threat Frequency (1–10)**
* **Behavioral Risk Factor** (inverse of behavior score)

Formula used:

* **Priority = (Impact × Frequency × Behavioral_Risk_Factor) / 100**
* Where **Behavioral_Risk_Factor = 100 − avg_behavior_score**

Output:

* Priority levels (Critical / High / Medium / Low)
* Recommendations automatically tailored to weak behavioral components + impact/frequency

---

### 3) ✅ Comprehensive Testing Suite (`test_system.py`)

Built:

* Unit tests for Fogg scoring correctness + clamping validation
* Unit tests for prioritization sorting + top-risk correctness
* Export validation tests (JSON file creation + content checks)
* Integration test using a realistic multi-department scenario

Final test outcome:

* **Overall Result: PASS**

---

### 4) 🏢 Organizational Assessment Tool (`org_assessment.py`)

Built a tool that:

* Defines department profiles (HR, Marketing, Finance, IT, Executives)
* Assesses behavioral posture by department
* Prioritizes common risks across departments
* Generates actionable recommendations (department + risk level)
* Exports full results to:

  * `reports/org_risk_report.json`

---

## 📊 Key Outcomes (What the Lab Demonstrated)

* Behavioral factors can dramatically change risk priority outcomes
* **Low ability** is frequently the biggest blocker, even when motivation is high
* Strong triggers (nudges, banners, simulations, reminders) can compensate for moderate motivation
* High-value targets (Executives/Finance) need **special handling**:

  * stronger controls
  * stronger triggers
  * targeted training and monitoring

---

## ✅ Result

By completing this lab, I successfully:

* Built a functional behavioral security scoring engine
* Prioritized cybersecurity risks using behavioral factors
* Validated correctness using unit + integration tests
* Generated organization-level risk reports and recommendations
* Exported structured JSON data for downstream security analytics

---

## 🌍 Why This Matters

Most security failures are not purely technical — they happen because people:

* forget (weak triggers)
* don’t know how (low ability)
* don’t feel urgency (low motivation)

Behavioral-driven security design improves:

* awareness program effectiveness
* policy adoption
* real-world behavior change
* risk-based resource allocation

---

## 🧰 Real-World Applications

* Security awareness program design (behavior-based interventions)
* Risk-based training prioritization (target weakest M/A/T)
* Department-level culture benchmarking
* Executive/VIP spear-phishing readiness programs
* Measuring policy effectiveness and adoption behavior
* Human risk analytics for compliance and governance

---

## 🏁 Conclusion

This lab demonstrated how **behavioral science** (B.J. Fogg Model) strengthens cybersecurity strategy by bridging the gap between technical controls and human behavior.

Traditional risk models focus on:

* **Impact × Likelihood**

This lab enhanced that with a human factor:

* **Impact × Frequency × Behavioral Risk Factor**

By measuring **Motivation, Ability, and Triggers**, we can identify the weakest component and design targeted interventions that drive real security behavior change.
