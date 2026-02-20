# 🛠️ Troubleshooting Guide - Lab 10: Kirkpatrick Four-Level Training Evaluation Model

> Environment: Ubuntu 24.04 | Python 3.12 | Virtual Environment (venv)

---

# 🔧 1. Virtual Environment Issues

---

## ❌ Issue: `ModuleNotFoundError: No module named 'pandas'`

### 🔎 Cause:

Virtual environment not activated or packages not installed.

### ✅ Solution:

```bash
cd ~/kirkpatrick_lab
source venv/bin/activate
pip install pandas numpy matplotlib seaborn scipy
```

Verify installation:

```bash
pip list
```

---

## ❌ Issue: `(venv)` not appearing in terminal

### 🔎 Cause:

Virtual environment not activated properly.

### ✅ Solution:

```bash
source venv/bin/activate
```

If still failing:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

---

# 📊 2. Data & CSV Issues

---

## ❌ Issue: `FileNotFoundError: data/training_data.csv`

### 🔎 Cause:

Incorrect working directory.

### ✅ Solution:

```bash
pwd
cd ~/kirkpatrick_lab
ls data/
```

Ensure files exist:

* training_data.csv
* criteria.json

---

## ❌ Issue: `ValueError: could not convert string to float`

### 🔎 Cause:

CSV formatting error (extra spaces, invalid characters).

### ✅ Solution:

Open file and verify numeric columns:

```bash
nano data/training_data.csv
```

Ensure:

* No trailing commas
* No missing numeric values
* No text in numeric columns

Optional cleanup:

```python
data = data.dropna()
```

---

## ❌ Issue: Division by zero error in calculations

### 🔎 Cause:

Incident count equals zero in denominator.

### ✅ Solution:

Ensure conditional checks exist:

```python
reduction_rate = reduction / total_before if total_before > 0 else 0
```

Already implemented in scripts.

---

# 📈 3. Statistical Calculation Issues

---

## ❌ Issue: `p-value = nan`

### 🔎 Cause:

Identical pre and post values or insufficient variation.

### ✅ Solution:

Verify dataset variability:

```python
print(data["pre_test"].describe())
print(data["post_test"].describe())
```

Ensure:

* Pre-test ≠ Post-test
* At least 2 samples

---

## ❌ Issue: `RuntimeWarning: invalid value encountered`

### 🔎 Cause:

Missing or NaN values in dataset.

### ✅ Solution:

```python
data = data.dropna()
```

Or handle:

```python
data.fillna(0, inplace=True)
```

---

# 📉 4. Visualization Problems

---

## ❌ Issue: Graph does not display

### 🔎 Cause:

Headless server environment (no GUI).

### ✅ Solution:

Use `plt.savefig()` instead of `plt.show()`
Already implemented in scripts.

Verify output:

```bash
ls visualizations/
```

---

## ❌ Issue: Permission denied saving PNG

### 🔎 Cause:

Directory permission issue.

### ✅ Solution:

```bash
chmod -R 755 visualizations
```

---

# 💰 5. ROI & Financial Calculation Issues

---

## ❌ Issue: ROI extremely large or negative

### 🔎 Cause:

Incorrect cost values in criteria.json.

### ✅ Solution:

Verify configuration:

```bash
cat data/criteria.json
```

Check:

* incident_cost
* training_cost_per_person

Ensure realistic business values.

---

## ❌ Issue: Negative incidents prevented

### 🔎 Cause:

Incidents_after > incidents_before.

### ✅ Solution:

ROI calculator already protects against negative values:

```python
if incidents_prevented < 0:
    incidents_prevented = 0.0
```

---

# 🗂 6. JSON Serialization Errors

---

## ❌ Issue: `TypeError: Object of type float32 is not JSON serializable`

### 🔎 Cause:

Numpy data types cannot be directly serialized.

### ✅ Solution:

Convert to native types:

```python
float(np_value)
int(np_value)
```

The `make_json_safe()` function already handles this.

---

# 🧪 7. Script Execution Errors

---

## ❌ Issue: `Permission denied`

### 🔎 Cause:

Script not executable.

### ✅ Solution:

```bash
chmod +x scripts/kirkpatrick_evaluator.py
```

---

## ❌ Issue: ImportError for local modules

Example:

```
ModuleNotFoundError: No module named 'statistics_helper'
```

### 🔎 Cause:

Script executed outside project directory.

### ✅ Solution:

```bash
cd ~/kirkpatrick_lab
python3 scripts/kirkpatrick_evaluator.py
```

---

# 🧠 8. Logical or Analytical Issues

---

## ❌ Issue: Effect size unusually small

### 🔎 Cause:

Minimal improvement in scores.

### ✅ Solution:

Investigate:

* Pre-test already high?
* Post-test too similar?
* Training content insufficient?

---

## ❌ Issue: Behavior improvement inconsistent

### 🔎 Cause:

Participants not applying knowledge.

### ✅ Solution:

Consider:

* Follow-up phishing simulations
* Manager reinforcement
* Refresher training

---

# 🔄 9. Performance Optimization

---

## Slow Script Execution?

### Causes:

* Large datasets
* Heavy plotting

### Optimization Tips:

```python
# Use vectorized operations instead of loops
data["improvement"] = data["post_test"] - data["pre_test"]
```

Avoid unnecessary loops where possible.

---

# 🛡 10. Enterprise-Level Debugging Strategy

If unexpected results occur:

### Step 1: Validate Data

```bash
head data/training_data.csv
```

### Step 2: Validate Criteria

```bash
cat data/criteria.json
```

### Step 3: Print Intermediate Values

Add debug prints:

```python
print(self.data.describe())
```

### Step 4: Validate Statistical Outputs

```python
print(t_stat, p_value)
```

### Step 5: Confirm Output Files

```bash
ls reports/
ls visualizations/
```

---

# 🧹 11. Clean Environment Reset

If environment becomes unstable:

```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn scipy
```

---

# 📦 12. Best Practices for Production Deployment

* Use requirements.txt
* Implement logging instead of print()
* Add input validation
* Use structured error handling (try/except)
* Add automated testing
* Integrate with CI/CD pipelines
* Secure financial calculation logic

---

# 🎯 Final Recommendation

If errors persist:

1. Re-run scripts in order
2. Confirm virtual environment
3. Validate dataset integrity
4. Confirm numeric consistency
5. Check file paths

---

## ✅ Troubleshooting Summary

| Category                  | Most Common Cause  | Quick Fix                  |
| ------------------------- | ------------------ | -------------------------- |
| Import Errors             | venv not activated | `source venv/bin/activate` |
| CSV Errors                | Formatting issue   | Clean CSV file             |
| JSON Errors               | Numpy types        | Convert to float/int       |
| Visualization Not Showing | Headless server    | Use `savefig()`            |
| ROI Incorrect             | Wrong cost config  | Verify criteria.json       |

---

# ✅ END OF LAB 10 TROUBLESHOOTING GUIDE
