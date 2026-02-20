# 🧪 Lab 12: Segmenting Audiences for Security Training

---

# 🎯 Lab Objectives

By completing this lab, I successfully:

- Implemented Python-based audience segmentation for cybersecurity training
- Generated structured employee datasets (200 records)
- Calculated risk scores using multiple weighted factors
- Segmented employees by:
  - Department
  - Risk Level
  - Training Urgency
- Applied the **AIDA (Attention, Interest, Desire, Action)** model
- Generated personalized training messages
- Analyzed message distribution and risk correlation
- Produced actionable training recommendations

---

# 🧠 Why This Lab Matters

Security awareness programs fail when training is generic.

This lab demonstrates how to:
- Identify high-risk groups
- Prioritize urgent training
- Personalize communication
- Use data to drive security decisions

This reflects **real-world Human Risk Management practices** used in enterprises.

---

## 📌 Prerequisites

-	Basic Python programming knowledge (functions, dictionaries, lists)
-	Understanding of CSV file operations
-	Familiarity with cybersecurity concepts
-	Text editor or Python IDE access

---

## 🖥 Environment
- Ubuntu 24.04.1 LTS (Cloud Lab Environment)
- User: `toor`
- Python 3.12.3

---

# 📂 Repository Structure

```

lab12-segmenting-audiences-for-security-training/
│
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│
├── employee_data_generator.py
├── audience_segmentation.py
├── aida_messaging.py
├── message_analysis.py
│
├── employees.csv
├── aida_messages.json
├── messages_for_delivery.csv
├── training_recommendations.csv
│
├── segment_department_*.csv
├── segment_risk_*.csv
└── segment_urgency_*.csv

```

---

# 🧩 Implementation Overview

## 1️⃣ Employee Data Generation

- 200 employees generated
- Departments: IT, Finance, HR, Marketing, Operations, Legal, Executive
- Risk calculated based on:
  - Access level
  - Training history
  - Incident history
  - Department adjustment
- Risk score normalized between 1–12

---

## 2️⃣ Segmentation Logic

### ✔ Department Segmentation
Grouped employees by department.

### ✔ Risk Segmentation
- Low Risk (1–3)
- Medium Risk (4–6)
- High Risk (7–9)
- Critical Risk (10–12)

### ✔ Training Urgency Segmentation
Calculated urgency score based on:
- Risk score
- Last training date
- Incident history
- Access level

Urgency levels:
- Immediate
- High Priority
- Medium Priority
- Low Priority

---

## 3️⃣ AIDA Messaging System

Each employee receives a personalized message based on:

Priority logic:
1. Incident history
2. Never trained
3. High-risk executives
4. High-risk IT
5. Medium-risk finance
6. General low-risk

Each message includes:
- Attention
- Interest (personalized by experience)
- Desire
- Action

---

## 4️⃣ Message Analysis

Performed:
- Category distribution analysis
- Department breakdown
- Risk correlation statistics
- Automated training recommendations

---

# 📊 Key Results

- 200 employee records generated
- 200 personalized AIDA messages created
- 16 segment CSV files generated
- 6 actionable training recommendations
- Clear risk prioritization insights

---

# 🔎 Real-World Relevance

This lab simulates:

- Enterprise security awareness segmentation
- Risk-based training assignment
- Executive and IT targeting
- Finance fraud prevention targeting
- Incident-driven refresher training

This approach scales to:
- 1,000+ employees
- Compliance tracking
- Regulatory mapping
- Role-based training assignment

---

# 🏁 What I Learned

- How to calculate risk-based scores programmatically
- How to segment datasets using Python
- How to apply behavioral communication models (AIDA)
- How to generate personalized messages at scale
- How to analyze effectiveness using statistics
- How to export operational-ready CSVs for deployment

---

# 📈 Expected Outcomes

After completing this lab:

✔ Risk-based training prioritization implemented  
✔ Segmentation exports generated  
✔ Personalized messages created  
✔ Recommendations automated  
✔ Data-driven insights produced  

---

# 🧠 Final Reflection

Security awareness becomes powerful when it is:

- Data-driven
- Risk-based
- Personalized
- Measurable

This lab bridges **technical Python implementation** with **strategic human risk management practices**.
