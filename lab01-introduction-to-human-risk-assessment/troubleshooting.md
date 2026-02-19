# Troubleshooting Guide — Lab 1: Introduction to Human Risk Assessment

## Issue 1: Database Permission Denied

### Cause
Apache (www-data) cannot access SQLite database.

### Resolution
```bash
sudo chown www-data:www-data ~/human-risk-assessment/data/assessment.db
sudo chmod 664 ~/human-risk-assessment/data/assessment.db
sudo chmod o+x ~
sudo chmod o+x ~/human-risk-assessment
sudo chmod o+x ~/human-risk-assessment/data
````

---

## Issue 2: Apache Not Serving Survey

### Cause

Apache not started or misconfigured.

### Resolution

```bash
sudo systemctl status apache2
sudo systemctl restart apache2
```

---

## Issue 3: PHP Not Writing to SQLite

### Cause

php-sqlite3 extension missing.

### Resolution

```bash
php -m | grep -i sqlite
sudo apt install -y php-sqlite3
sudo systemctl restart apache2
```

---

## Issue 4: Python Import Errors

### Cause

Virtual environment not active.

### Resolution

```bash
source ~/human-risk-assessment/.venv/bin/activate
python -m pip list
```

---

## Issue 5: Empty Risk Scores

### Cause

Survey data not generated or scoring script not executed.

### Resolution

```bash
python3 generate_sample_data.py
python3 analyze_data.py
```

---

## Issue 6: Apache Permission Traversal Errors

### Cause

Apache cannot traverse home directories.

### Resolution

Ensure execute permission:

```bash
sudo chmod o+x ~
sudo chmod o+x ~/human-risk-assessment
sudo chmod o+x ~/human-risk-assessment/data
```
