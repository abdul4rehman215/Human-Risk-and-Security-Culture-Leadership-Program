# 🛠️ Troubleshooting Guide — Lab 16: ROI of Security Culture Programs

> This document outlines common issues encountered during the lab and the systematic steps used to resolve them.

---

# 1️⃣ Data Generation Issues

## ❌ Issue: Generated values look unrealistic

### Symptoms
- Phishing rate drops too quickly (e.g., from 15% to 1% in 2 months)
- Security incidents fall to zero instantly
- Compliance reaches 100% immediately
- Negative or extremely high program costs

### 🔎 Root Causes
- Incorrect improvement curve (linear instead of exponential)
- Excessive random noise
- Incorrect clipping bounds
- Unrealistic baseline assumptions

### ✅ Resolution Steps
1. Verify baseline values:
   - Phishing rate: 10–20%
   - Incidents: 5–10 per month
   - Compliance: 60–75%
2. Ensure exponential decay factor (`k = 0.18`) is moderate.
3. Use `np.clip()` to enforce realistic bounds.
4. Confirm cost components:
   - Setup cost applied only first month
   - Operational cost grows gradually

### ✔ Validation Command
```bash
head -n 5 ../data/security_metrics.csv
````

---

# 2️⃣ CSV File Not Created

## ❌ Issue: `security_metrics.csv` not found

### Symptoms

```text
FileNotFoundError: Data file not found
```

### 🔎 Root Causes

* Wrong working directory
* Relative path incorrect
* Script not executed from `/scripts`

### ✅ Resolution Steps

1. Confirm location:

```bash
pwd
```

2. Navigate correctly:

```bash
cd ~/security_roi_lab/scripts
```

3. Re-run generator:

```bash
python3 data_generator.py
```

4. Confirm file exists:

```bash
ls -lh ../data/
```

---

# 3️⃣ ROI Always Negative

## ❌ Issue: ROI shows negative values for all months

### Symptoms

* Monthly ROI consistently < 0%
* Cumulative ROI never becomes positive
* Payback period returns None

### 🔎 Root Causes

* Incident cost per event too low
* Savings categories missing from calculation
* Program costs too high
* Benefit columns not numeric

### ✅ Resolution Steps

1. Verify incident cost assumption:

```python
incident_cost_per_incident = 25000
```

2. Confirm benefits calculation:

```python
df["total_benefits"] = (
    df["incident_savings"] +
    df["productivity_gain"] +
    df["compliance_savings"]
)
```

3. Ensure no NaN values:

```python
df.fillna(0)
```

4. Re-run:

```bash
python3 roi_calculator.py
```

---

# 4️⃣ ROI Calculation Errors

## ❌ Issue: Missing required columns

### Symptoms

```text
ValueError: Missing required columns: [...]
```

### 🔎 Root Causes

* CSV modified manually
* Data generator script altered
* Wrong input file passed

### ✅ Resolution Steps

1. Regenerate data:

```bash
python3 data_generator.py
```

2. Confirm CSV headers:

```bash
head -n 1 ../data/security_metrics.csv
```

3. Verify expected columns:

* program_cost
* incident_savings
* productivity_gain
* compliance_savings
* total_benefits

---

# 5️⃣ Visualizations Not Rendering (Headless Ubuntu 24.04)

## ❌ Issue: Charts fail to generate

### Symptoms

* Backend error
* No PNG files created
* Matplotlib display errors

### 🔎 Root Cause

Ubuntu cloud environments lack GUI display server.

### ✅ Resolution

Set matplotlib backend:

```bash
export MPLBACKEND=Agg
```

Verify:

```bash
echo $MPLBACKEND
```

Re-run:

```bash
python3 visualization.py
```

---

# 6️⃣ Visualization Files Not Created

## ❌ Issue: PNG files missing

### 🔎 Root Causes

* Wrong output directory
* Script terminated early
* Missing required columns

### ✅ Resolution Steps

1. Confirm directory exists:

```bash
ls -la ../visualizations
```

2. Manually create if needed:

```bash
mkdir -p ../visualizations
```

3. Re-run script.

---

# 7️⃣ Dashboard Won't Start

## ❌ Issue: Dash app does not launch

### Symptoms

* Port already in use
* Import errors
* Blank page

### 🔎 Root Causes

* Port 8050 occupied
* Dash not installed
* Firewall blocking port

### ✅ Resolution Steps

### Check port usage

```bash
sudo netstat -tuln | grep 8050
```

If in use, kill process or change port in script.

### Verify Dash installation

```bash
pip list | grep dash
```

### Verify Plotly installation

```bash
pip list | grep plotly
```

### Restart dashboard

```bash
python3 interactive_dashboard.py
```

---

# 8️⃣ Virtual Environment Issues

## ❌ Issue: ModuleNotFoundError

### 🔎 Root Cause

Virtual environment not activated.

### ✅ Resolution

```bash
source ~/security_roi_lab/security_roi_env/bin/activate
```

Confirm:

```bash
which python
```

Should point to:

```
.../security_roi_env/bin/python
```

---

# 9️⃣ Permission Errors

## ❌ Issue: Permission denied when executing script

### ✅ Fix

```bash
chmod +x script_name.py
```

Or execute directly:

```bash
python3 script_name.py
```

---

# 🔟 JSON Summary Not Exporting

## ❌ Issue: `roi_summary.json` missing

### 🔎 Root Causes

* `export_results()` not called
* Path incorrect
* Write permissions issue

### ✅ Resolution

Verify in `main()`:

```python
calculator.export_results(
    "../reports/roi_detailed_results.csv",
    "../reports/roi_summary.json"
)
```

Confirm directory:

```bash
ls -la ../reports
```

---

# 🔐 Security & Operational Considerations

Even though this is a modeling lab, in real environments:

* Protect financial data files
* Do not expose dashboards publicly without authentication
* Avoid running Dash in debug mode in production
* Use HTTPS and reverse proxy (Nginx) for deployment

---

# 📌 Best Practices Learned

✔ Always validate data before financial modeling
✔ Use cumulative ROI for strategic analysis
✔ Visualizations enhance executive communication
✔ Use realistic assumptions for credibility
✔ Automate reporting for repeatability

---

# 🏁 Final Verification Checklist

```bash
ls ../data/security_metrics.csv
ls ../reports/roi_detailed_results.csv
ls ../reports/roi_summary.json
ls ../visualizations/
```

All files present = Lab completed successfully ✅
