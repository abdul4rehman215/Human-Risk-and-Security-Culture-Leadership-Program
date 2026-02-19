# 🛠️ Troubleshooting Guide — Lab 6: Building Strategic Risk Plans

---

## 1. Python Package Import Errors

### Problem
```

ModuleNotFoundError: No module named 'pandas'

````

### Cause
Required packages are not installed in the environment.

### Solution
```bash
pip3 install --upgrade pandas matplotlib seaborn numpy
````

Verify installation:

```bash
python3 -c "import pandas, matplotlib, seaborn, numpy; print('All packages OK')"
```

---

## 2. CSV File Not Found Errors

### Problem

```
FileNotFoundError: risk_alignment_matrix.csv
```

### Cause

The framework script was not executed before running visualization or reporting modules.

### Solution

Run in this order:

```bash
python3 risk_framework.py
python3 role_risk_assessment.py
python3 risk_visualization.py
python3 role_visualization.py
python3 risk_report_generator.py
```

Verify file existence:

```bash
ls *.csv
```

---

## 3. JSON Loading Errors

### Problem

```
json.decoder.JSONDecodeError
```

### Cause

Corrupted or partially written JSON file.

### Solution

Validate JSON:

```bash
python3 -m json.tool prioritized_action_plan.json
```

If invalid:

* Regenerate by re-running:

```bash
python3 role_risk_assessment.py
```

---

## 4. Empty DataFrames in Reports

### Problem

Report shows zero counts or missing summaries.

### Cause

Input CSV files may be empty or incorrectly generated.

### Solution

Check row counts:

```bash
python3 -c "import pandas as pd; print(pd.read_csv('role_based_risk_assessment.csv').shape)"
```

Expected:

```
(20, 7)
```

Re-run assessment if necessary.

---

## 5. Visualization Not Saving

### Problem

PNG files are not generated.

### Possible Causes

* Missing matplotlib backend
* File permission issues
* Script exited early due to missing data

### Solutions

Check backend:

```bash
python3 -c "import matplotlib; print(matplotlib.get_backend())"
```

If needed:

```bash
pip3 install python3-tk
```

Check directory permissions:

```bash
ls -ld .
```

Ensure `plt.savefig()` and `plt.close()` are present in scripts.

---

## 6. Incorrect Risk Scores

### Problem

Risk scores appear too high or too low.

### Possible Causes

* Incorrect risk weight values
* Incorrect multiplier calculations
* Culture score outside 0–1 range

### Solution

Verify calculations manually:

```bash
python3
>>> from risk_framework import RiskBehaviorCultureFramework
>>> f = RiskBehaviorCultureFramework()
>>> f.calculate_risk_score("phishing", "low", 0.3)
```

Ensure:

* Behavior multipliers are correct
* Culture score is between 0.0 and 1.0

---

## 7. Markdown Report Formatting Issues

### Problem

`risk_report.md` appears malformed.

### Cause

Text editor encoding or newline issues.

### Solution

Regenerate:

```bash
python3 risk_report_generator.py
```

View using:

```bash
less risk_report.md
```

Ensure UTF-8 encoding.

---

## 8. Action Timeline Plot Missing Labels

### Problem

Scatter plot generated but labels overlap.

### Cause

Too many data points close together.

### Solution

Adjust scatter size scaling inside:

```
role_visualization.py
```

Increase spacing or reduce marker size multiplier:

```python
plt.scatter(df["timeline_weeks"], df["avg_score"], s=df["instances"] * 30)
```

---

## 9. Seaborn Style Errors

### Problem

```
ValueError: style not found
```

### Cause

Seaborn not installed or incompatible version.

### Solution

```bash
pip3 install seaborn --upgrade
```

Test:

```bash
python3 -c "import seaborn; print(seaborn.__version__)"
```

---

## 10. Performance Issues on Larger Datasets

### Problem

Scripts run slowly with expanded data.

### Cause

Large pivot operations and group-by calculations.

### Solution

* Optimize using vectorized Pandas operations
* Avoid excessive loops
* Use:

```python
df.groupby(..., observed=True)
```

for categorical optimization.

---

## 11. Numpy Serialization Errors in JSON

### Problem

```
TypeError: Object of type float64 is not JSON serializable
```

### Cause

Numpy numeric types cannot be directly serialized.

### Solution

Convert to native Python types:

```python
float(value)
int(value)
```

Or use:

```python
json.dump(data, f, default=str)
```

---

## 12. Incorrect Priority Distribution

### Problem

Unexpected number of critical/high entries.

### Cause

Priority threshold definitions may be altered.

### Expected Priority Thresholds

| Risk Score | Priority |
| ---------- | -------- |
| ≥ 8.0      | critical |
| ≥ 6.0      | high     |
| ≥ 4.0      | medium   |
| < 4.0      | low      |

Verify in:

```
role_risk_assessment.py
```

---

# Recommended Execution Order (Clean Run)

```bash
python3 risk_framework.py
python3 risk_visualization.py
python3 role_risk_assessment.py
python3 role_visualization.py
python3 risk_report_generator.py
```

---

# Validation Checklist

✔ 60 alignment scenarios generated
✔ 20 role-risk combinations created
✔ 6+ visualizations saved
✔ Action plan JSON generated
✔ Markdown report generated
✔ No JSON validation errors
✔ No missing CSV files

---

# Final Advice

If errors occur:

1. Re-run scripts in correct order
2. Verify file existence before loading
3. Validate JSON files
4. Confirm package installation
5. Check Python version (3.12.3 recommended)

---

End of Troubleshooting Guide
Lab 6 – Building Strategic Risk Plans
