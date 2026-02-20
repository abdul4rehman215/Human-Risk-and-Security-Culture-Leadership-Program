# 🧪 Lab 17: Compliance vs. Impact Metrics 
  
> **Focus:** Measuring security awareness effectiveness using **Compliance Metrics** vs **Impact Metrics**  

---

## 📌 Overview

Security culture programs are often evaluated using **compliance metrics** (e.g., training completion rates).  
But **compliance does not guarantee reduced risk**.

This lab builds a complete measurement pipeline to:

- Define and explain compliance vs impact metrics
- Generate realistic datasets for both metric types
- Analyze each metric type with Python
- Create visualizations for reporting
- Compare both metric types together to find gaps and insights
- Generate stakeholder-ready reports and recommendations

---

## 🎯 Objectives

By the end of this lab, I was able to:

- Differentiate between **compliance metrics** and **impact metrics**
- Implement Python tools to collect, analyze, and visualize both metric types
- Generate data-driven reports to evaluate awareness effectiveness
- Interpret results to make informed decisions for security culture initiatives

---

## ✅ Prerequisites

- Basic Python programming knowledge
- Understanding of data analysis concepts
- Familiarity with security awareness training principles
- Linux command line experience

---

## 🧰 Tools & Technologies Used

- **Python 3.x**
- **pandas, numpy** for analysis
- **matplotlib, seaborn** for visualization
- Headless safe plotting via `savefig()`  
  *(if needed: `export MPLBACKEND=Agg`)*

> **Environment:** Ubuntu 24.04 (Cloud Lab) • User: `toor`  
> **Folder:** `~/metrics_lab`

---

## 🗂️ Repository Structure

```text
lab17-compliance-vs-impact-metrics/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│   
├── scripts/
│   ├── metric_definitions.py
│   ├── data_generator.py
│   ├── compliance_analyzer.py
│   ├── compliance_visualizer.py
│   ├── impact_analyzer.py
│   ├── impact_visualizer.py
│   └── integrated_dashboard.py
│   
├── reports/
│   ├── compliance_metrics.csv
│   ├── impact_metrics.csv
│   ├── compliance_report.txt
│   ├── impact_report.txt
│   └── integrated_recommendations.txt
│   
├── visualizations/
│   ├── dept_comparison.png
│   ├── compliance_trends.png
│   ├── correlation_heatmap.png
│   ├── behavioral_trends.png
│   ├── maturity_progression.png
│   ├── incident_correlation.png
│   └── executive_dashboard.png
```

---

## ✅ What I Did in This Lab

### **Task 1: Understanding Metric Types**

* Created the project directory: `~/metrics_lab`
* Built `metric_definitions.py` to print:

  * Definitions
  * Examples
  * Key differences
* Executed script to confirm output formatting

### **Task 2: Compliance Metrics Pipeline**

* Generated compliance dataset (`compliance_metrics.csv`) including:

  * Training completion rates
  * Policy acknowledgment rates
  * Phishing click rates
  * Assessment pass rates
  * Derived compliance score
* Built `compliance_analyzer.py` to compute:

  * Summary stats (mean/median/std/min/max)
  * Department performance ranking
  * Trend analysis
  * Threshold gap detection
  * Executive summary + recommendations
  * Output report saved to: `compliance_report.txt`
* Built `compliance_visualizer.py` to generate:

  * Department comparison chart
  * Compliance trends dashboard
  * Correlation heatmap

### **Task 3: Impact Metrics Pipeline**

* Generated impact dataset (`impact_metrics.csv`) including:

  * Voluntary reporting counts
  * Security discussions initiated
  * Proactive behaviors
  * Peer coaching instances
  * Security incidents (downward trend)
  * Culture maturity score
* Built `impact_analyzer.py` to compute:

  * Behavioral change (first month vs last month)
  * Culture maturity categorization
  * Proactive behaviors vs incidents relationship
  * Incident reduction trend
  * Executive summary + recommendations
  * Output report saved to: `impact_report.txt`
* Built `impact_visualizer.py` to generate:

  * Behavioral trend charts
  * Maturity progression chart
  * Incident correlation scatter plot

### **Task 4: Integrated Comparison**

* Built `integrated_dashboard.py` to:

  * Merge compliance + impact datasets on `date, department`
  * Run correlation analysis between:

    * compliance score vs maturity
    * training completion vs voluntary reporting
    * phishing click rate vs incidents
  * Identify departments that may show:

    * **High compliance but weak culture maturity**
  * Produce an executive dashboard image
  * Generate strategic recommendations saved to:
    `integrated_recommendations.txt`

---

## 📊 Key Insights / Learnings

* ✅ **Compliance metrics** confirm completion and adherence (audit value)
* ✅ **Impact metrics** reflect culture change and actual risk reduction
* ⚠️ High compliance can still result in:

  * weak reporting culture
  * continued risky behavior
  * incidents remaining high
* 📈 True effectiveness requires **tracking both**:

  * Compliance (what was done)
  * Impact (what changed)

---

## 🌍 Why This Matters (Real-World Relevance)

Security leaders often struggle to justify program effectiveness.

This lab shows how to build a **data-driven measurement strategy** that:

* translates awareness activity into culture outcomes
* detects “checkbox compliance” traps
* improves executive reporting
* enables targeted interventions by department
* supports security culture ROI discussions

---

## ✅ Results Produced

### Data Outputs

* `compliance_metrics.csv`
* `impact_metrics.csv`

### Reports

* `compliance_report.txt`
* `impact_report.txt`
* `integrated_recommendations.txt`

### Visualizations (PNG)

* `dept_comparison.png`
* `compliance_trends.png`
* `correlation_heatmap.png`
* `behavioral_trends.png`
* `maturity_progression.png`
* `incident_correlation.png`
* `executive_dashboard.png`

---

## 🏁 Conclusion

This lab demonstrated that **measuring security culture requires more than compliance**.

By combining compliance + impact metrics:

* program success becomes measurable beyond “completion rates”
* culture maturity can be tracked objectively
* risk reduction becomes visible through incident trends
* executives gain confidence in awareness program decisions
