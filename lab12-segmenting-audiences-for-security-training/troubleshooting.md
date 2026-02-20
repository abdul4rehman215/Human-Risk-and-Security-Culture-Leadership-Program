# 🛠️ Troubleshooting Guide - Lab 12: Segmenting Audiences for Security Training  

> Environment: Ubuntu 24.04.1 LTS  
> Python Version: 3.12.3  

---

# 1️⃣ CSV File Not Found Error

## ❌ Error Example
FileNotFoundError: CSV file not found: employees.csv

## 🔎 Cause
The segmentation or messaging scripts were executed before generating the employee dataset.

## ✅ Solution
1. Ensure you are inside the correct directory:
```bash
   pwd
```

2. Generate employee data first:

   ```bash
   python3 employee_data_generator.py
   ```
3. Confirm file exists:

   ```bash
   ls employees.csv
   ```

---

# 2️⃣ Risk Scores Appear Incorrect (All Zero or Unexpected Values)

## ❌ Symptom

* All employees show risk_score = 0
* Risk distribution seems unrealistic

## 🔎 Cause

Possible issues:

* Incorrect risk calculation logic
* Numeric conversion failure
* Missing risk adjustment factors

## ✅ Solution

1. Review `_risk_points_access()`, `_risk_points_training()`, `_risk_points_incident()` functions.
2. Ensure risk_score normalization:

   ```python
   risk_score = max(1, min(12, adjusted))
   ```
3. Verify numeric conversion in segmentation:

   ```python
   row["risk_score"] = int(row.get("risk_score", 0))
   ```

---

# 3️⃣ Empty Segment Files Generated

## ❌ Symptom

Segment CSV files created but contain only headers.

## 🔎 Cause

* Segmentation thresholds may not match dataset
* Employees not meeting category conditions
* Data loading issue

## ✅ Solution

1. Print sample employee records before segmentation:

   ```python
   print(self.employees[:5])
   ```
2. Confirm segmentation logic ranges:

   * Low Risk (1–3)
   * Medium Risk (4–6)
   * High Risk (7–9)
   * Critical Risk (10–12)
3. Ensure employee list is not empty:

   ```python
   print(len(self.employees))
   ```

---

# 4️⃣ AIDA Messages Not Personalized

## ❌ Symptom

Messages appear generic without name or experience-based customization.

## 🔎 Cause

* Personalization logic not triggered
* Missing `years_experience` field
* Incorrect template mapping

## ✅ Solution

1. Verify personalization function:

   ```python
   def personalize_interest(...)
   ```
2. Ensure numeric conversion:

   ```python
   row["years_experience"] = int(row.get("years_experience", 0))
   ```
3. Print category determination:

   ```python
   print(employee["employee_id"], category)
   ```

---

# 5️⃣ Incorrect Department Distribution (Negative Values Observed)

## ❌ Symptom

Negative percentage or impossible values in department breakdown.

## 🔎 Cause

Copy/paste artifact or incorrect manual output formatting.

## ✅ Resolution

Re-run analysis:

```bash
python3 message_analysis.py
```

Correct breakdown verified:

```
Department: Finance (Total: 30)
  - medium_risk_finance: 18 (60.0%)
  - incident_history: 10 (33.3%)
  - never_trained: 1 (3.3%)
  - low_risk_general: 1 (3.3%)
```

---

# 6️⃣ JSON Decode Error

## ❌ Error Example

json.JSONDecodeError: Expecting value

## 🔎 Cause

* Corrupted or partially written `aida_messages.json`
* Script interrupted during execution

## ✅ Solution

1. Delete corrupted file:

   ```bash
   rm aida_messages.json
   ```
2. Regenerate:

   ```bash
   python3 aida_messaging.py
   ```

---

# 7️⃣ Permission Denied Errors

## ❌ Error Example

Permission denied: segment_department_it.csv

## 🔎 Cause

Insufficient write permissions.

## ✅ Solution

Check ownership:

```bash
ls -l
```

Fix permissions:

```bash
chmod 644 *.csv *.json
```

---

# 8️⃣ Training Recommendations CSV Not Generated

## ❌ Symptom

`training_recommendations.csv` missing after running analysis.

## 🔎 Cause

No messages loaded into analyzer.

## ✅ Solution

Ensure workflow order:

1. Generate employees
2. Run segmentation
3. Generate AIDA messages
4. Run message analysis

Correct order:

```bash
python3 employee_data_generator.py
python3 audience_segmentation.py
python3 aida_messaging.py
python3 message_analysis.py
```

---

# 9️⃣ Incorrect Message Category Assignment

## ❌ Symptom

High-risk employees categorized as low_risk_general.

## 🔎 Cause

Priority order in `determine_message_category()` may not match expected logic.

## ✅ Solution

Verify category priority order:

1. incident_history
2. never_trained
3. executives high risk
4. IT high risk
5. finance medium risk
6. default

Ensure conditional statements are evaluated correctly.

---

# 🔟 Segment File Line Count Confusion

## ❓ Question

Why does total line count exceed 200?

## ✅ Explanation

Each segment CSV includes:

* 1 header line
* Multiple overlapping segmentation exports

Since employees belong to:

* Department segment
* Risk segment
* Urgency segment

The combined total lines across files will exceed 200.

---

# 🧠 Best Practice Recommendations

✔ Always run scripts in correct order
✔ Validate intermediate outputs before proceeding
✔ Use print debugging during development
✔ Verify numeric conversions for CSV imports
✔ Maintain consistent data schema across scripts

---

# 🏁 Final Validation Checklist

| Validation Step                        | Status |
| -------------------------------------- | ------ |
| employees.csv generated                | ✅      |
| segment_*.csv files created            | ✅      |
| aida_messages.json generated           | ✅      |
| messages_for_delivery.csv generated    | ✅      |
| training_recommendations.csv generated | ✅      |
| Risk distribution logical              | ✅      |
| Department totals correct              | ✅      |
| No negative or impossible values       | ✅      |

---

# 🎯 Lab 12 Troubleshooting Complete
