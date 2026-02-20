# 🛠 Troubleshooting Guide - Lab 13: Data-Driven Behavior Change

---

# 🔧 Environment & Setup Issues

---

## 1️⃣ Virtual Environment Not Activating

### ❌ Issue

`
bash: source: venv/bin/activate: No such file or directory
`

### ✅ Possible Causes

* Virtual environment was not created
* Wrong directory
* Typo in path

### ✅ Solution

```bash
cd ~/behavior-lab
python3 -m venv venv
source venv/bin/activate
```

Verify activation:

```bash
which python
```

Expected:
`
/home/toor/behavior-lab/venv/bin/python
`

---

## 2️⃣ pip Packages Not Found

### ❌ Issue

`
ModuleNotFoundError: No module named 'pandas'
`

### ✅ Cause

Packages not installed inside virtual environment.

### ✅ Solution

Activate venv and reinstall:

```bash
source venv/bin/activate
pip install pandas numpy matplotlib seaborn
```

Verify:

```bash
pip list
```

---

## 3️⃣ Permission Denied When Running Script

### ❌ Issue

`
Permission denied: ./generate_data.py
`

### ✅ Cause

Script not executable.

### ✅ Solution

```bash
chmod +x scripts/generate_data.py
chmod +x scripts/analyze_behavior.py
chmod +x scripts/create_charts.py
chmod +x scripts/export_for_web.py
chmod +x scripts/detect_patterns.py
```

---

# 📊 Data & Analysis Issues

---

## 4️⃣ CSV Format Errors

### ❌ Issue
`
KeyError: 'Pre_Score'
`

### ✅ Cause

CSV column mismatch or typo.

### ✅ Solution

Check header:

```bash
head data/behavior_data.csv
```

Ensure exact column names:

```
Pre_Score
Post_Score
Phishing_Test_1
Password_Compliance
...
```

CSV must match template exactly.

---

## 5️⃣ JSON Export Not Updating

### ❌ Issue

Dashboard shows old values.

### ✅ Cause

Did not re-run export script.

### ✅ Solution

```bash
cd scripts
python3 export_for_web.py
```

Then refresh browser.

---

## 6️⃣ Analysis Results Seem Incorrect

### ❌ Issue

Unexpected averages or risk counts.

### ✅ Debug Steps

Check dataset:

```bash
wc -l data/behavior_data.csv
```

Verify sample:

```bash
head data/behavior_data.csv
```

Re-generate data:

```bash
python3 generate_data.py
```

---

# 📈 Visualization Issues

---

## 7️⃣ Charts Not Generated

### ❌ Issue

No PNG files in visualizations folder.

### ✅ Check

```bash
ls visualizations/
```

If empty:

### ✅ Solution

```bash
cd scripts
python3 create_charts.py
```

Check for matplotlib errors.

---

## 8️⃣ Matplotlib Backend Error (Headless Server)

### ❌ Issue

```
cannot connect to X server
```

### ✅ Solution

Ensure no GUI backend required.
Use default backend (already safe in Ubuntu cloud).

If needed:

```python
import matplotlib
matplotlib.use("Agg")
```

---

# 🌐 Dashboard & Web Issues

---

## 9️⃣ Dashboard Not Loading

### ❌ Issue

Browser shows blank page.

### ✅ Check

Open:

```
http://localhost:8080/dashboard.html
```

Check console (F12 → Console).

---

## 🔟 JSON Fetch Error

### ❌ Issue

`
Failed to load dashboard_data.json
`

### ✅ Causes

* export_for_web.py not run
* Wrong directory
* Not running from web folder

### ✅ Fix

```bash
cd ~/behavior-lab/web
python3 -m http.server 8080
```

Ensure file exists:

```bash
ls dashboard_data.json
```

---

## 1️⃣1️⃣ Port Already in Use

### ❌ Issue

```
OSError: [Errno 98] Address already in use
```

### ✅ Solution

Use different port:

```bash
python3 -m http.server 8081
```

---

# 🕵 Pattern Detection Issues

---

## 1️⃣2️⃣ Correlation Returns NaN

### ❌ Issue

Correlation values show `nan`.

### ✅ Cause

Insufficient variation in data.

### ✅ Fix

Re-generate larger dataset:

```bash
python3 generate_data.py
```

Modify to:

```python
generate_behavior_data(200)
```

---

## 1️⃣3️⃣ pattern_insights.json Not Created

### ❌ Issue

No file in data directory.

### ✅ Solution

```bash
cd scripts
python3 detect_patterns.py
```

Verify:

```bash
ls ../data/pattern_insights.json
```

---

# 📦 Performance & Scaling Issues

---

## 1️⃣4️⃣ Slow Performance with Large Dataset

### Cause

CSV processing for thousands of employees.

### Solutions

* Use pandas vectorization (already implemented)
* Move to database (PostgreSQL)
* Use chunk processing
* Use Dask or Spark for scaling

---

# 🔐 Security & Data Handling Concerns

---

## 1️⃣5️⃣ Sensitive Employee Data Exposure

### Risk

Storing raw CSV publicly.

### Mitigation

* Use access control
* Remove employee IDs before sharing reports
* Encrypt storage
* Use role-based dashboard access

---

# 🧠 Common Logical Mistakes

---

## 1️⃣6️⃣ Confusing Behavior Score with Knowledge Score

Knowledge improvement ≠ secure behavior.

Behavior score includes:

* Compliance
* MFA
* Reporting
* Phishing resilience

---

## 1️⃣7️⃣ Assuming High Incident Reports Are Always Bad

In some cases:

* Reporting shows engagement
* Zero reporting may indicate apathy

Balance is key.

---

# 🏁 Final Debug Checklist

Before Submission Ensure:

* ✅ behavior_data.csv generated
* ✅ analysis_results.json created
* ✅ pattern_insights.json created
* ✅ dashboard_data.json exported
* ✅ PNG charts generated
* ✅ Web dashboard loads successfully
* ✅ No console errors in browser

---

# 🎯 Summary

This troubleshooting guide ensures:

* Stable Python environment
* Correct data format
* Reliable statistical calculations
* Functional visualizations
* Working interactive dashboard
* Proper pattern detection logic
