# 🛠 Troubleshooting Guide — Lab 05: Role-Based Risk Identification

> This document outlines common issues encountered during the lab and their resolutions.

---

# 1️⃣ JSON Decode Errors

## ❌ Issue
Error while loading JSON files:

`json.decoder.JSONDecodeError: Expecting ',' delimiter`

## 🔍 Cause
- Missing comma
- Extra bracket
- Incorrect quotation marks
- Improper formatting

## ✅ Resolution

Validate JSON syntax:

```bash
python3 -m json.tool organizational_roles.json
python3 -m json.tool cti_data.json
```

If errors appear:
- Check for missing commas
- Ensure all strings use double quotes
- Confirm proper closing braces/brackets

---

# 2️⃣ Virtual Environment Not Activated

## ❌ Issue
`ModuleNotFoundError:`


ModuleNotFoundError: No module named 'pandas'

## 🔍 Cause
Virtual environment is not active.

## ✅ Resolution

Activate environment:

```bash
source risk_env/bin/activate
```

Reinstall dependencies if required:

```bash
pip install pandas numpy matplotlib
```
`id="ld7s2r"`

Verify:

```bash
python3 -c "import pandas, numpy, matplotlib; print('OK')"
```

---

# 3️⃣ Empty Risk Analysis Results

## ❌ Issue
Output shows:

`[ERROR] No role data loaded`

## 🔍 Cause
- JSON file not loaded
- File path incorrect
- load_organizational_data() failed

## ✅ Resolution

Confirm files exist:

```bash
ls -lh
```

Ensure correct filenames:
- organizational_roles.json
- cti_data.json

Re-run:

```bash
python3 run_analysis.py
```

---

# 4️⃣ Visualization Not Generated

## ❌ Issue
`risk_analysis_charts.png` not created.

## 🔍 Cause
- matplotlib backend issue
- Missing Tkinter
- Script terminated early

## ✅ Resolution

Install Tk backend if needed:

```bash
pip install python-tk
```

Ensure script completes without errors.

Confirm file creation:

```bash
ls -lh risk_analysis_charts.png
```

---

# 5️⃣ Permission Errors

## ❌ Issue

`Permission denied`

## 🔍 Cause
Script not executable.

## ✅ Resolution

Make scripts executable:

```bash
chmod +x role_risk_analyzer.py
chmod +x run_analysis.py
chmod +x advanced_classifier.py
chmod +x filter_high_risk_roles.py
```

---

# 6️⃣ Incorrect Risk Scores

## ❌ Issue
Risk scores seem unrealistic (too high or too low).

## 🔍 Possible Causes
- CTI severity values misconfigured
- Department multipliers incorrect
- Base weighting formula modified
- Role attributes incorrectly entered

## ✅ Resolution

Verify:
- JSON data values (1–5 scale)
- Weighting formula in `_base_score()`
- Department multiplier mapping
- CTI severity values

Recalculate manually for one role to confirm.

---

# 7️⃣ Advanced Classification Not Generating Files

## ❌ Issue
`advanced_risk_classification.json` not found.

## 🔍 Cause
File loading failure or script not executed.

## ✅ Resolution

Run explicitly:

```bash
python3 advanced_classifier.py
```

Confirm output:

```bash
ls -lh advanced_risk_classification.json
```
---

# 8️⃣ High-Risk Filter Script Shows Zero Results

## ❌ Issue

`Total high-risk roles found: 0`

## 🔍 Cause
Threshold too high.

## ✅ Resolution

Lower threshold in script:

```python
filter_high_risk_roles("comprehensive_risk_report.json", 50)
```

Re-run:

```bash
python3 filter_high_risk_roles.py
```

---

# 🔐 Security Best Practice Reminder

Always:
- Validate external JSON input
- Sanitize file paths
- Use virtual environments
- Apply least privilege on script execution
- Avoid exposing sensitive data in reports

---

# ✅ Final Verification Checklist

✔ Virtual environment activated  
✔ Dependencies installed  
✔ JSON validated  
✔ Risk analysis executed  
✔ Reports generated  
✔ Advanced classification completed  
✔ High-risk filtering confirmed  
✔ Visualization charts created  

---

# 🎯 Summary

This lab integrates:
- Risk scoring
- Threat intelligence
- Automation
- Reporting
- Visualization
- Classification logic

Troubleshooting ensures:
- Reproducibility
- Stability
- Accuracy
- Operational readiness

Proper debugging is essential in real-world security operations where automation tools must be reliable and validated.
