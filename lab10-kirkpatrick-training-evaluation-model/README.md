# 🧪 Lab 10: Kirkpatrick's Four-Level Training Evaluation Model

# 📌 Overview

This lab implements **Kirkpatrick’s Four-Level Training Evaluation Model** using Python, statistical analysis, and data visualization. 

The project simulates a corporate security awareness training evaluation and demonstrates:

The evaluation includes:

1️⃣ **Level 1 – Reaction**  
2️⃣ **Level 2 – Learning**  
3️⃣ **Level 3 – Behavior**  
4️⃣ **Level 4 – Results (ROI & Business Impact)** 

* Quantitative training effectiveness measurement
* Statistical validation of learning improvement
* Behavioral change analysis
* ROI and business impact calculation
* Department-level analytics
* Automated reporting and professional visualization
* JSON reporting for Stakeholders

This implementation reflects real-world Learning & Development (L&D) analytics practices used in enterprise environments.

---

# 🎯 Objectives

By completing this lab, I was able to:

- Apply Kirkpatrick’s four-level model in real-world evaluation
- Perform statistical significance testing (paired t-test)
- Calculate effect size (Cohen’s d)
- Measure behavioral impact via incident reduction
- Calculate ROI and business value
- Generate professional analytics visualizations (stakeholder-ready)
- Produce structured JSON reports

---

## 📌 Prerequisites

- Basic Python programming knowledge
- Understanding of REST APIs and JSON
- Familiarity with Linux command line
- Basic cybersecurity concepts
- Understanding of web technologies (HTML, CSS)

---

# 🧰 Lab Environment

| Component | Value |
|-----------|--------|
| OS | Ubuntu 24.04 |
| User | toor |
| Python | 3.12.x |
| Virtual Environment | venv |
| Libraries | pandas, numpy, matplotlib, seaborn, scipy |

---

# 📂 Project Structure

```

lab10-kirkpatrick-training-evaluation-model/
│   
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│   
├── data/
│   ├── criteria.json
│   └── training_data.csv
│   
├── reports/
│   └── evaluation_results_TIMESTAMP.json
│   
├── scripts/
│   ├── kirkpatrick_evaluator.py
│   ├── department_analysis.py
│   ├── statistics_helper.py
│   ├── roi_calculator.py
│   └── custom_analysis.py
│   
├── visualizations/
│   ├── kirkpatrick_overview_TIMESTAMP.png
│   └── department_comparison_TIMESTAMP.png
│   
└── venv/

```

---

# 🧩  Kirkpatrick Model Implementation

## 🟢 Level 1 – Reaction
- Mean Reaction Score: **4.22**
- 80% participants ≥ threshold (4.0)

## 🔵 Level 2 – Learning
- Pre-Test Avg: 64.4
- Post-Test Avg: 84.6
- Avg Improvement: 20.2
- Passing Rate: 86.7%
- Cohen’s d: ~2.1 (Very Large Effect)
- p-value < 0.001 (Statistically Significant)
- 95% confidence interval

## 🟡 Level 3 – Behavior
- Incidents Before: 51
- Incidents After: 17
- Reduction: 34
- Reduction Rate: 66.7%

## 🔴 Level 4 – Results
- Avg Business Impact: 8.53
- Total Training Cost: $7,500
- Cost Savings: $340,000
- ROI: **4433%**

---

# 📊 Statistical Methods Used

* Paired t-test (`scipy.stats.ttest_rel`)
* Cohen’s d effect size
* Confidence interval calculation
* Correlation analysis
* Composite scoring

All statistical calculations are automated and reproducible.

---

# 📊 Visualization Outputs

The lab generates:

- Reaction distribution histogram
- Pre vs Post scatter comparison
- Incident reduction bar chart
- Business impact by department
- Department comparison dashboard

--- 

# 📊 Business Impact Summary

| Level    | Outcome                               |
| -------- | ------------------------------------- |
| Reaction | Strong satisfaction                   |
| Learning | Statistically significant improvement |
| Behavior | 66.7% reduction in incidents          |
| Results  | 4433% ROI                             |

The training demonstrates measurable and financially validated effectiveness.

---

# 🚀 How to Run

## 1️⃣ Clone or Navigate

```bash
cd kirkpatrick_lab
```

## 2️⃣ Activate Virtual Environment

```bash
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## 4️⃣ Run Main Evaluation

```bash
python3 scripts/kirkpatrick_evaluator.py
```

## 5️⃣ Run Department Analysis

```bash
python3 scripts/department_analysis.py
```

## 6️⃣ Run Custom Analysis

```bash
python3 scripts/custom_analysis.py
```

---


# 💼 Real-World Relevance

This framework mirrors:

- Corporate L&D evaluation systems
- HR analytics dashboards
- Compliance training measurement
- Security awareness ROI tracking
- Enterprise-level training impact measurement

---

# 🔐 Why This Matters

Organizations invest heavily in training programs.  
Without measurement:

- Effectiveness is unknown
- ROI is unclear
- Stakeholder confidence drops
- Budgets may be cut

Kirkpatrick’s model ensures:

- Data-driven decision making
- Measurable business impact
- Continuous improvement
- Strategic alignment

---

# 🏁 Expected Outcomes

✔ Full 4-level Kirkpatrick implementation  
✔ Statistical testing  
✔ Effect size measurement  
✔ ROI and cost-benefit analysis  
✔ Department comparison  
✔ JSON reporting  
✔ Professional visualizations  

---

# 🔍 Advanced Extensions

Future improvements may include:

* Longitudinal impact tracking
* Control group comparison
* Predictive modeling (regression)
* Dashboard integration
* Automated LMS data ingestion
* Qualitative sentiment analysis

---

## 📜 License

Educational use only.
Designed for training analytics and cybersecurity evaluation practice.

---

# 📌 Conclusion

This lab demonstrates how to translate training evaluation theory into a fully operational analytics pipeline using Python.

The structured approach enables organizations to:

- Quantify training effectiveness
- Validate business value
- Improve continuously
- Present professional analytics to stakeholders

---

## Result

This lab transforms training evaluation from subjective feedback to measurable, statistical, and financially validated performance analysis.

It mirrors real-world L&D analytics workflows used in enterprise environments.

---

# 👨‍💻 Author

Abdul Rehman

Human Risk & Security Culture Leadership Program  
Lab Series – Advanced Training Evaluation
