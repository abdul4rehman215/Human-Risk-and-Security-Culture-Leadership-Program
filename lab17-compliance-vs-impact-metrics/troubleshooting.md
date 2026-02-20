## 🛠️ Troubleshooting Guide - Lab 17: Compliance vs Impact Metrics (Ubuntu 24.04)

> This document covers common technical and logical issues encountered while performing the lab, along with structured troubleshooting steps and resolutions.

---

# 1️⃣ CSV Files Not Found

## ❗ Error Example

```text
FileNotFoundError: [Errno 2] No such file or directory: 'compliance_metrics.csv'
```

## 🔍 Root Cause

* `data_generator.py` was not executed
* Executed in a different directory
* Files were accidentally deleted

## ✅ Resolution Steps

1. Verify current directory:

```bash
pwd
```

Expected:

```text
/home/toor/metrics_lab
```

2. Regenerate datasets:

```bash
python3 data_generator.py
```

3. Confirm files exist:

```bash
ls -lh *.csv
```

Expected:

```text
compliance_metrics.csv
impact_metrics.csv
```

---

# 2️⃣ Python Module Import Errors

## ❗ Error Example

```text
ModuleNotFoundError: No module named 'pandas'
```

## 🔍 Root Cause

Required packages not installed in environment.

## ✅ Resolution

Install dependencies:

```bash
pip3 install pandas matplotlib seaborn numpy
```

If using virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib seaborn numpy
```

Verify installation:

```bash
python3 -c "import pandas, matplotlib, seaborn, numpy"
```

No output = success.

---

# 3️⃣ Matplotlib Not Displaying Plots (Headless Environment)

## ❗ Problem

Plots are not visible when running on cloud VM.

## 🔍 Root Cause

No GUI display server available.

## ✅ Resolution

This lab uses:

```python
plt.savefig()
```

If needed, set backend:

```bash
export MPLBACKEND=Agg
```

Then rerun visualizer scripts.

Verify images:

```bash
ls -lh *.png
```

---

# 4️⃣ Date Parsing Errors

## ❗ Error Example

```text
ValueError: time data does not match format '%Y-%m'
```

## 🔍 Root Cause

CSV date format mismatch.

Expected format:

```text
YYYY-MM
```

Example:

```text
2025-02
```

## ✅ Resolution

Check CSV:

```bash
head compliance_metrics.csv
```

Ensure format consistency.

If necessary, adjust parsing:

```python
pd.to_datetime(self.df["date"], errors="coerce")
```

---

# 5️⃣ Division by Zero Errors

## ❗ Possible Error

```text
ZeroDivisionError
```

## 🔍 Root Cause

Percentage change calculation where start value = 0.

## ✅ Resolution

Safe checks were included:

```python
pct = ((end - start) / start * 100.0) if start != 0 else 0.0
```

If modifying code, ensure guard conditions remain.

---

# 6️⃣ Correlation Produces NaN

## ❗ Example

```text
Correlation: nan
```

## 🔍 Root Cause

* Constant values in column
* Missing values
* Insufficient data points

## ✅ Resolution

1. Ensure dataset generated correctly
2. Drop missing values:

```python
df = df.dropna()
```

3. Confirm numeric types:

```python
df.dtypes
```

---

# 7️⃣ Empty Gap Identification Output

## ❗ Problem

```text
No gaps found.
```

## 🔍 Explanation

All metrics met defined thresholds.

This is not an error.

To test gap logic:

* Lower thresholds
* Adjust generator baseline values

---

# 8️⃣ Visualizations Overlapping Labels

## ❗ Problem

Date labels overlapping.

## ✅ Resolution

Already handled:

```python
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
```

If needed:

```python
plt.gcf().autofmt_xdate()
```

---

# 9️⃣ Incorrect Effectiveness Ratio Results

## 🔍 Possible Causes

* Scaling denominator too small
* Improper normalization
* Extreme values in dataset

## ✅ Debug Steps

Print scaled values:

```python
print(proactive_scaled)
print(incidents_scaled)
```

Verify normalization formula:

```python
(value - min) / (max - min)
```

Ensure denominator includes small epsilon:

```python
+ 1e-9
```

---

# 🔟 Integrated Dashboard Merge Issues

## ❗ Error

Merged dataset empty.

## 🔍 Root Cause

* Date mismatch
* Department name mismatch
* Different formats

## ✅ Resolution

Check unique values:

```python
print(self.compliance["department"].unique())
print(self.impact["department"].unique())
```

Ensure exact match.

Confirm date format consistency.

---

# 1️⃣1️⃣ Performance Issues with Large Datasets

If scaling to real organizational data:

## Potential Issues

* Memory usage
* Slow groupby operations
* Large visualization rendering time

## Optimization Strategies

* Use chunked CSV loading
* Pre-aggregate data
* Reduce plot DPI
* Use vectorized pandas operations
* Export summary tables instead of full dataset

---

# 1️⃣2️⃣ Logical Troubleshooting (Security Interpretation)

## Issue: High Compliance, Low Impact

Possible causes:

* Training not engaging
* Knowledge not applied
* Lack of reinforcement
* No leadership support

Resolution:

* Add scenario-based exercises
* Increase peer coaching
* Implement leadership messaging
* Measure behavioral indicators

---

# 1️⃣3️⃣ Debugging Strategy Used in This Lab

Structured approach:

1. Validate data generation
2. Validate CSV integrity
3. Confirm numeric conversions
4. Confirm aggregation logic
5. Validate trend calculations
6. Confirm correlations make logical sense
7. Validate executive summaries align with raw data

---

# 1️⃣4️⃣ Validation Checklist

Before submitting lab:

✔ CSV files exist
✔ PNG files generated
✔ TXT reports generated
✔ No traceback errors
✔ Correlations computed
✔ Incident reduction calculated
✔ Dashboard image created

---

# 1️⃣5️⃣ Best Practices Learned

* Always validate data types
* Always protect division operations
* Use aggregation before visualization
* Use threshold-based gap detection
* Separate compliance from impact analytics
* Never assume correlation implies causation

---

# Final Troubleshooting Summary

Most technical issues fall into:

1. Missing files
2. Missing dependencies
3. Headless plotting configuration
4. Data formatting inconsistencies

Most logical issues fall into:

1. Misinterpreting compliance as success
2. Ignoring incident trends
3. Not correlating behavior with outcomes

---
