# 🛠️ Lab 18 — Troubleshooting Guide: Communication Strategies for Security Culture  

---

## 🔎 Overview

This document outlines common technical and logical issues encountered during the implementation of:

- Golden Circle framework
- Communication plan generator
- Email automation system
- Scheduler
- Metrics tracking
- Communication dashboard

Each issue includes:

- Problem description
- Root cause
- Resolution steps
- Prevention best practices

---

# 1️⃣ Import Errors Between Scripts

## ❌ Issue
```

ModuleNotFoundError: No module named 'email_config'

```

## 🔍 Root Cause
Running scripts from incorrect directory, causing Python import path mismatch.

Example:
```

python3 scripts/email_scheduler.py

```
while being in the parent directory.

## ✅ Solution

Run from inside the scripts directory:

```

cd scripts
python3 email_scheduler.py

```

OR modify `PYTHONPATH`:

```

export PYTHONPATH=$(pwd)

```

## 🛡️ Prevention
Keep related modules in the same directory and execute from that location.

---

# 2️⃣ JSON File Write Errors

## ❌ Issue
```

FileNotFoundError: [Errno 2] No such file or directory: 'data/email_schedule.json'

````

## 🔍 Root Cause
Directory does not exist before writing file.

## ✅ Solution

Ensure directory creation before writing:

```python
os.makedirs(os.path.dirname(filename), exist_ok=True)
````

This was implemented in all file save functions.

## 🛡️ Prevention

Always validate directory existence before file operations.

---

# 3️⃣ Template Variables Not Substituting

## ❌ Issue

```
KeyError: 'training_completion'
```

## 🔍 Root Cause

Mismatch between template placeholders and provided keyword arguments.

Example:
Template expects:

```
{training_completion}
```

But data dictionary did not include that key.

## ✅ Solution

Ensure all placeholders are provided:

```python
subject, body = self.templates.generate_email(audience, **template_data)
```

Validate template keys carefully.

## 🛡️ Prevention

Keep consistent naming conventions and test template rendering separately.

---

# 4️⃣ Engagement Rate Above 100%

## ❌ Issue

Executive engagement shows:

```
120.0%
```

## 🔍 Root Cause

Formula:

```
(Opens + Clicks) / Sent
```

If recipients both open and click, combined value can exceed sent count.

## ✅ Solution Options

Option A:
Calculate based on unique users instead.

Option B:
Use:

```
max(opens, clicks) / sent
```

Option C:
Keep current method but document interpretation.

(Current implementation documents behavior.)

---

# 5️⃣ Date Parsing Errors

## ❌ Issue

```
ValueError: time data does not match format '%Y-%m-%d'
```

## 🔍 Root Cause

Date format inconsistency.

Expected:

```
YYYY-MM-DD
```

## ✅ Solution

Use consistent formatting:

```python
datetime.now().strftime("%Y-%m-%d")
```

When parsing:

```python
datetime.strptime(date_string, "%Y-%m-%d")
```

## 🛡️ Prevention

Standardize date format globally across system.

---

# 6️⃣ Schedule Not Processing Emails

## ❌ Issue

No emails sent during scheduler execution.

## 🔍 Root Cause

`send_date` > current date.

Scheduler processes only due emails:

```
if send_date <= current_date:
```

## ✅ Solution

Simulate sending:

```python
scheduler.process_due_emails(datetime.now())
```

Or adjust start_date manually for testing.

---

# 7️⃣ Metrics File Not Found in Dashboard

## ❌ Issue

Dashboard prints:

```
Metrics file not found.
```

## 🔍 Root Cause

`communication_metrics.py` not executed before dashboard.

## ✅ Solution

Run:

```
python3 scripts/communication_metrics.py
```

Then:

```
python3 scripts/communication_dashboard.py
```

---

# 8️⃣ HTML Templates Not Rendering Properly

## ❌ Issue

Generated HTML files appear malformed.

## 🔍 Root Cause

Unescaped characters or incorrect indentation.

## ✅ Solution

Validate HTML in browser.
Ensure no missing format keys.

---

# 9️⃣ Scheduler Summary Count Incorrect

## ❌ Issue

Mismatch in expected totals.

Expected:

* Executive: 12
* Manager: 24
* Employee: 48
* Total: 84

## 🔍 Root Cause

Incorrect month loop or frequency multiplier.

## ✅ Solution

Review:

```python
for m in range(months):
```

Ensure months=12.

---

# 🔟 Permissions Issues

## ❌ Issue

```
Permission denied
```

## 🔍 Root Cause

Script not executable.

## ✅ Solution

```
chmod +x script_name.py
```

OR run directly:

```
python3 script_name.py
```

---

# 1️⃣1️⃣ Log File Not Updating

## ❌ Issue

`email_log.json` empty.

## 🔍 Root Cause

`save_log()` not called.

## ✅ Solution

Ensure:

```python
self.email_sender.save_log("logs/email_log.json")
```

is executed after sending.

---

# 1️⃣2️⃣ Incorrect Engagement Interpretation

## ❌ Issue

High engagement misinterpreted as success.

## 🔍 Root Cause

Clicks may include phishing simulation behavior.

## ✅ Solution

Segment link types:

* ROI report
* Toolkit
* Training module

Evaluate link intent.

---

# 1️⃣3️⃣ Data Corruption in JSON Files

## ❌ Issue

```
json.decoder.JSONDecodeError
```

## 🔍 Root Cause

Interrupted write operation.

## ✅ Solution

Delete corrupted file and regenerate:

```
rm data/email_schedule.json
python3 scripts/email_scheduler.py
```

---

# 1️⃣4️⃣ Environment Compatibility Issues

## ❌ Issue

Scripts fail on older Python versions.

## 🔍 Root Cause

Use of modern formatting and type hints.

## ✅ Solution

Ensure Python 3.10+:

```
python3 --version
```

---

# 1️⃣5️⃣ Best Practice Validation Checklist

Before final submission:

* [ ] All directories created
* [ ] All JSON files present
* [ ] Scheduler created 84 total entries
* [ ] Metrics generated successfully
* [ ] Dashboard displays overview
* [ ] No import errors
* [ ] All scripts executable
* [ ] Logs saved correctly

---

# 🎯 Final Notes

Most issues in automation systems stem from:

* Path mismanagement
* Inconsistent data formats
* Template mismatches
* Improper execution order

This lab reinforces:

✔ Modular Python design
✔ Data validation
✔ Structured logging
✔ Reproducible automation workflows
✔ Defensive programming practices

---
