# 🛠 Troubleshooting Guide - Lab 09: ADDIE Model for Training Development

# 🔍 Overview

> This document outlines common issues encountered during the ADDIE workflow lab and provides structured solutions.

The lab includes:

- Multiple Python modules
- JSON file persistence
- Directory creation
- Inter-module imports
- Interactive CLI execution
- Workflow orchestration

Because the project is modular and file-based, most issues relate to:

- Path handling
- File permissions
- Execution context
- Data persistence
- User input errors

---

# 🚨 Issue 1: ImportError Between Modules

## ❌ Error Example

`
ModuleNotFoundError: No module named 'addie_framework'
`

## 📌 Root Cause

Python cannot locate modules inside the `scripts/` directory when running from project root.

## ✅ Solution

Always run the workflow from the project root:

```bash
cd ~/addie_training_lab
./scripts/complete_addie_workflow.py
````

The workflow script already adds the scripts directory to `sys.path`:

```python
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
```

If running modules individually, ensure:

```bash
cd ~/addie_training_lab/scripts
python3 addie_framework.py
```

---

# 🚨 Issue 2: Permission Denied Error

## ❌ Error Example

`
bash: ./scripts/addie_framework.py: Permission denied
`

## 📌 Root Cause

Script is not executable.

## ✅ Solution

Grant execution permission:

```bash
chmod +x scripts/*.py
```

Then re-run:

```bash
./scripts/addie_framework.py
```

---

# 🚨 Issue 3: JSON File Not Found

## ❌ Error Example

```
FileNotFoundError: [Errno 2] No such file or directory
```

## 📌 Root Cause

* Directory not created
* Incorrect relative path
* Running from wrong directory

## ✅ Solution

Verify directory structure:

```bash
ls -la
```

Ensure folders exist:

```bash
mkdir -p analyze design develop implement evaluate data reports
```

The workflow auto-creates them, but manual execution may require directory creation.

---

# 🚨 Issue 4: Data Not Persisting Between Phases

## 📌 Root Cause

Running phases independently without saving framework state.

## ✅ Solution

Use the integrated workflow:

```bash
./scripts/complete_addie_workflow.py
```

Or ensure project state is saved:

```python
self.framework.save_project()
```

Project state is stored in:

```
data/Security_Awareness_Training_TIMESTAMP.json
```

---

# 🚨 Issue 5: Incorrect User Input (Non-Numeric Values)

## ❌ Example

Entering text instead of numbers:

`
Enter average pre-test score percent: abc
`

## 📌 Root Cause

Invalid input type.

## ✅ Solution

The script already handles this safely:

```python
try:
    pre_val = float(pre_avg)
except ValueError:
    pre_val = 0.0
```

If incorrect values are entered, simply re-run the phase.

---

# 🚨 Issue 6: Completion Rate Calculation Incorrect

## 📌 Root Cause

Progress values outside 0–100 range.

## ✅ Solution

The implementation automatically constrains values:

```python
tracking[name]["progress_percent"] = max(0, min(100, progress_val))
```

Ensure numeric input between 0 and 100.

---

# 🚨 Issue 7: Workflow Stops Midway

## 📌 Possible Causes

* Keyboard interrupt (Ctrl+C)
* Terminal closed
* Input skipped
* File system permission issue

## ✅ Recovery Steps

1. Verify saved artifacts:

   ```bash
   find . -maxdepth 2 -type f
   ```

2. Re-run the workflow:

   ```bash
   ./scripts/complete_addie_workflow.py
   ```

---

# 🚨 Issue 8: ROI Calculation Produces Zero or Negative Value

## 📌 Root Cause

* Incidents not reduced
* Training cost too high
* Incorrect numeric input

## ✅ Understanding the Formula

```
ROI (%) = ((Savings - Cost) / Cost) × 100
```

Savings calculated as:

```
incident_reduction × assumed_cost_per_incident
```

Adjust inputs realistically.

---

# 🚨 Issue 9: Directory Structure Corrupted

## 📌 Root Cause

Files moved or deleted accidentally.

## ✅ Fix

Recreate structure:

```bash
mkdir -p ~/addie_training_lab/{analyze,design,develop,implement,evaluate,scripts,data,reports}
```

Restore scripts from repository.

---

# 🚨 Issue 10: Running Script with python Instead of python3

## ❌ Error Example

`
SyntaxError due to Python version mismatch
`

## ✅ Solution

Always use Python 3:

```bash
python3 script_name.py
```

Or use executable shebang:

```bash
#!/usr/bin/env python3
```

---

# 🔐 Security-Relevant Considerations

Because this lab simulates a **Security Awareness Training Program**, consider:

* Protecting JSON files containing training metrics
* Avoiding hardcoded credentials
* Restricting write permissions
* Storing reports securely
* Avoid exposing internal incident statistics

Optional hardening:

```bash
chmod 600 data/*.json
```

---

# 📁 Verification Checklist

Run:

```bash
find . -maxdepth 2 -type f | sort
```

Confirm presence of:

* analyze/
* design/
* develop/
* implement/
* evaluate/
* data/
* reports/
* scripts/

All phases should show `complete` when running:

```bash
./scripts/addie_framework.py
```

---

# ✅ Best Practices Learned

* Always run from project root
* Keep modular structure clean
* Validate user inputs
* Persist state between phases
* Document outputs thoroughly
* Use structured reporting
* Maintain clear folder separation

---

# 🎯 Final Note

If all five phases show:

```
Completion: 100%
```

Then the ADDIE workflow executed successfully and the training development lifecycle is fully documented and measurable.

---

# ✅ End of Troubleshooting Guide – Lab 09
