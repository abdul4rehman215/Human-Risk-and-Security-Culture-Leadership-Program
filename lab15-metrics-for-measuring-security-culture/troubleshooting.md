# 🛠️ Troubleshooting Guide -  Lab 15: Metrics for Measuring Security Culture

> This section documents common technical issues encountered while building the database, analytics modules, and dashboard — along with structured fixes.

---

## 1️⃣ Database Connection Errors

### ❌ Problem
- `sqlite3.OperationalError: unable to open database file`
- Database file missing
- Permission denied errors

### 🔎 Verification Commands
```bash
ls -lh data/security_culture.db
````

If file exists but permission issue:

```bash
chmod 644 data/security_culture.db
```

If SQLite CLI missing:

```bash
sudo apt update
sudo apt install -y sqlite3
```

### ✅ Fix Summary

* Ensure `data/` directory exists
* Ensure database file path matches code (`data/security_culture.db`)
* Confirm virtual environment activated
* Check file permissions

---

## 2️⃣ Sample Data Not Appearing

### ❌ Problem

* Queries return empty results
* Dashboard shows 0 values
* API returns empty datasets

### 🔎 Verification

```bash
sqlite3 data/security_culture.db
.tables
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM security_training;
```

### ✅ Fix

Re-run data generation script:

```bash
python scripts/generate_sample_data.py
```

Then re-run:

```bash
python scripts/culture_analyzer.py
python scripts/trend_analyzer.py
```

---

## 3️⃣ Flask Application Not Starting

### ❌ Problem

* `Address already in use`
* Port 5000 not accessible
* Module not found errors

### 🔎 Check Port Usage

```bash
sudo lsof -i :5000
```

Kill conflicting process if necessary.

### 🔎 Check Installed Packages

```bash
pip list
```

Ensure:

* Flask
* pandas
* numpy

### 🔎 Ensure Virtual Environment Active

```bash
source venv/bin/activate
```

### ✅ Fix

Restart Flask:

```bash
python scripts/dashboard_app.py
```

---

## 4️⃣ D3.js Visualizations Not Rendering

### ❌ Problem

* Blank charts
* No data in graphs
* Console errors in browser

### 🔎 Check API Endpoints

```bash
curl -s http://localhost:5000/api/culture-metrics | head
curl -s http://localhost:5000/api/trend-data | head
curl -s http://localhost:5000/api/department-metrics | head
```

If API returns error JSON:

* Check Flask logs
* Verify database path
* Confirm analyzer modules working

### 🔎 Browser Console

Open DevTools → Console → Check for:

* CORS errors
* JSON parsing errors
* 500 server errors

### ✅ Fix

* Restart Flask server
* Clear browser cache
* Confirm D3 library loads from CDN

---

## 5️⃣ JSON Report Files Not Generated

### ❌ Problem

`culture_report.json` or `trend_report.json` missing

### 🔎 Verify

```bash
ls -lh data/
```

### ✅ Fix

Run:

```bash
python scripts/culture_analyzer.py
python scripts/trend_analyzer.py
```

Check file sizes afterward.

---

## 6️⃣ Foreign Key Constraint Errors

### ❌ Problem

`sqlite3.IntegrityError: FOREIGN KEY constraint failed`

### 🔎 Cause

Attempt to insert child record before employee exists.

### ✅ Fix

Ensure:

1. Employees inserted first
2. `PRAGMA foreign_keys = ON;` enabled
3. Database cleared before regeneration

To reset DB:

```bash
rm data/security_culture.db
python scripts/setup_database.py
python scripts/generate_sample_data.py
```

---

## 7️⃣ Dashboard Loads But Metrics Look Wrong

### Possible Causes

* Randomized data changed
* Days-back filter too small
* Data not regenerated after schema update

### 🔎 Validate Period Window

Check in analyzer:

```python
generate_comprehensive_report(days_back=90)
```

Increase days if needed.

---

## 8️⃣ Performance Issues (Large Dataset Scenario)

If scaled beyond lab size:

### Optimization Suggestions

* Add DB indexes:

```sql
CREATE INDEX idx_training_date ON security_training(completion_date);
CREATE INDEX idx_phishing_date ON phishing_simulations(simulation_date);
```

* Cache report results
* Reduce repeated DB connections

---

## 🔐 Security Notes (Important for Real Deployment)

⚠️ This lab runs Flask in debug mode:

`
app.run(debug=True)
`

In production:

* Disable debug mode
* Use Gunicorn or uWSGI
* Add authentication
* Use HTTPS
* Restrict DB file permissions
* Implement input validation
* Add logging and monitoring

---

# ✅ Final Validation Checklist

✔ Database file exists
✔ Tables created successfully
✔ Sample data generated
✔ JSON reports generated
✔ Flask app running
✔ API endpoints returning JSON
✔ Dashboard rendering charts
✔ Trend analysis working
✔ No console errors
