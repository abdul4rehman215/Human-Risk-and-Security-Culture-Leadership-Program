# 🛠️ Troubleshooting Guide - Lab 19: Executing Long-Term Security Programs

> This document outlines common issues encountered during the execution of the long-term security program lab and their respective solutions.

---

# 1️⃣ JSON Parsing Errors

## ❌ Issue
Error message such as:
`
json.decoder.JSONDecodeError: Expecting ',' delimiter
`

## 🔎 Cause
- Missing comma
- Incorrect bracket placement
- Invalid quotation marks
- Trailing comma in JSON file

## ✅ Solution
Validate JSON syntax:

```bash
python3 -m json.tool config/program_config.json
````

If validation fails:

* Check all `{}` and `[]` are properly closed
* Ensure double quotes are used (not single quotes)
* Remove trailing commas

---

# 2️⃣ Strategy Report Not Found

## ❌ Issue

`
Strategy report not found. Run strategy_engine.py first.
`

## 🔎 Cause

`project_planner.py` executed before `strategy_engine.py`.

## ✅ Solution

Run in correct order:

```bash
python3 scripts/strategy_engine.py
python3 scripts/project_planner.py
```

---

# 3️⃣ Project Plan JSON Invalid

## ❌ Issue

`
Project plan JSON invalid.
`

## 🔎 Cause

Corrupted or manually modified `project_plan.json`.

## ✅ Solution

Regenerate the project plan:

```bash
rm reports/project_plan.json
python3 scripts/project_planner.py
```

---

# 4️⃣ Metrics History File Missing

## ❌ Issue

`
Metrics history not found. Run monitoring_system.py first.
`

## 🔎 Cause

`automated_reporting.py` executed before monitoring system generated metrics.

## ✅ Solution

Execute:

```bash
python3 scripts/monitoring_system.py
python3 scripts/automated_reporting.py
```

---

# 5️⃣ Pandas or Matplotlib Not Installed

## ❌ Issue

`
ModuleNotFoundError: No module named 'pandas'
`

## 🔎 Cause

Required Python libraries not installed.

## ✅ Solution

Install dependencies:

```bash
pip3 install pandas matplotlib
```

Verify installation:

```bash
python3 -c "import pandas, matplotlib"
```

---

# 6️⃣ Permission Denied When Executing Script

## ❌ Issue

`
Permission denied
`

## 🔎 Cause

Script not executable.

## ✅ Solution

Make script executable:

```bash
chmod +x scripts/<script_name>.py
```

Example:

```bash
chmod +x scripts/strategy_engine.py
```

---

# 7️⃣ Incorrect Working Directory

## ❌ Issue

Files not found even though they exist.

## 🔎 Cause

Script executed from wrong directory causing relative path issues.

## ✅ Solution

Always execute from project root:

```bash
cd ~/security_program
python3 scripts/project_planner.py
```

---

# 8️⃣ Unrealistic Metric Values

## ❌ Issue

Metrics appear unrealistic (e.g., incident_count too high).

## 🔎 Cause

Random number simulation used for lab purposes.

## ✅ Solution

Modify random ranges inside:

```python
random.randint(min, max)
```

Or replace with realistic data from actual incident logs.

---

# 9️⃣ Charts Not Generated

## ❌ Issue

No PNG files created in charts folder.

## 🔎 Cause

* Matplotlib backend issue
* Incorrect metrics_history.csv format
* No data records

## ✅ Solution

Verify:

```bash
ls data/metrics_history.csv
```

Ensure file contains records.

If necessary:

```bash
python3 scripts/monitoring_system.py
python3 scripts/automated_reporting.py
```

---

# 🔟 Date Calculation Errors

## ❌ Issue

Incorrect timeline calculations.

## 🔎 Cause

Improper date format or manual edit in configuration.

## ✅ Solution

Ensure format:

```
YYYY-MM-DD
```

Example:

```json
"start_date": "2024-01-01"
```

---

# 1️⃣1️⃣ Governance Framework Not Generated

## ❌ Issue

```
Missing config/program_config.json
```

## 🔎 Cause

Configuration file not present.

## ✅ Solution

Ensure:

```bash
ls config/program_config.json
```

If missing, recreate configuration file.

---

# 🔒 Security Best Practice Notes

* Never store real production credentials inside configuration files.
* Do not expose generated reports publicly if they contain sensitive organizational metrics.
* Ensure proper file permissions when deploying similar frameworks in real environments.

---

# 🎯 Final Validation Checklist

Before considering the lab complete, verify:

✔ `strategy_report.json` exists
✔ `project_plan.json` exists
✔ `task_list.csv` created
✔ `metrics_history.csv` populated
✔ `status_report.json` generated
✔ Charts present inside `automated_reports/charts/`
✔ `governance_framework.json` created

---

# 🏁 Resolution Summary

Most issues in this lab are related to:

* Execution order
* Missing dependencies
* Incorrect file paths
* JSON formatting errors

Following proper script execution order and validating JSON files resolves 90% of encountered issues.

---

**Lab 19 troubleshooting completed successfully.**
