# 🛠 Troubleshooting Guide - Lab 20: Final Security Culture Program Assessment

---

# 🔎 Overview

This document outlines common technical issues encountered while building and executing the Security Culture Assessment framework and provides structured resolution steps.

The lab involves:

- Python scripting
- JSON data processing
- Visualization with matplotlib
- File packaging and directory handling

Because multiple components interact, troubleshooting must be systematic.

---

# 1️⃣ ModuleNotFoundError (matplotlib / numpy / pandas / seaborn)

## ❗ Problem

When running:

`
python3 scripts/report_generator.py
`

receive:

`
ModuleNotFoundError: No module named 'matplotlib'
`

## 🎯 Cause

Required Python libraries are not installed in the environment.

## ✅ Solution

Install required packages:

```bash
pip3 install matplotlib numpy pandas seaborn
````

Verify installation:

```bash
python3 -c "import matplotlib, numpy; print('Modules OK')"
```

---

# 2️⃣ JSON Decode Error

## ❗ Problem

`
json.decoder.JSONDecodeError: Expecting value
`

## 🎯 Cause

One of the JSON files in `data/` is:

* Corrupted
* Partially written
* Manually edited incorrectly

## ✅ Solution

Validate JSON syntax:

```bash
python3 -m json.tool data/training_metrics.json
```

If invalid:

* Regenerate data:

  ```bash
  python3 scripts/generate_data.py
  ```

---

# 3️⃣ assessment_results.json Not Found

## ❗ Problem

Running report generator produces:

`
[!] Error: Missing reports/assessment_results.json
`

## 🎯 Cause

Assessment analyzer was not executed before report generation.

## ✅ Solution

Run in proper order:

```bash
python3 scripts/assessment_analyzer.py
python3 scripts/report_generator.py
```

---

# 4️⃣ Charts Not Saving / Empty Image Files

## ❗ Problem

PNG files exist but are empty or corrupted.

## 🎯 Possible Causes

* Missing write permissions
* Incorrect matplotlib backend
* Script terminated early

## ✅ Solutions

### Check backend:

```python
import matplotlib
print(matplotlib.get_backend())
```

Ensure `Agg` backend is set in script:

```python
matplotlib.use("Agg")
```

### Check permissions:

```bash
ls -ld reports/
chmod -R 755 reports/
```

---

# 5️⃣ Incorrect Maturity Scores (Unrealistic Values)

## ❗ Problem

Overall score >100 or negative values.

## 🎯 Cause

* Weights not summing to 1.0
* Missing clamp logic
* Data outside 0–100 range

## ✅ Solutions

### Verify weights in `config.py`

```python
CATEGORY_WEIGHTS = {
    "awareness": 0.25,
    "behavior": 0.30,
    "culture": 0.25,
    "outcomes": 0.20
}
```

Ensure sum = 1.0

### Validate values before calculations

Clamp logic implemented:

```python
def _clamp(value, low=0.0, high=100.0):
    return max(low, min(high, float(value)))
```

---

# 6️⃣ Division by Zero Errors

## ❗ Problem

Errors during score calculation.

## 🎯 Cause

Metrics such as:

* total_incidents = 0
* response_time = 0
* empty survey dataset

## ✅ Solution

The script includes safe fallbacks:

* Default response_time = 48 hours
* Empty survey returns 0 score
* Defensive try/except for missing files

If manually editing data, ensure:

* No zero denominators
* All fields present

---

# 7️⃣ Permission Denied When Running Scripts

## ❗ Problem

`
Permission denied
`

## 🎯 Cause

Script not executable.

## ✅ Solution

```bash
chmod +x scripts/*.py
```

Or run directly:

```bash
python3 scripts/script_name.py
```

---

# 8️⃣ Deliverables ZIP Not Created

## ❗ Problem

Packaging script runs but no ZIP file created.

## 🎯 Cause

* Missing `deliverables/` directory
* shutil.make_archive failure
* Insufficient permissions

## ✅ Solution

Check directory:

```bash
ls -l deliverables/
```

Re-run:

```bash
python3 scripts/package_deliverables.py
```

Ensure disk space is sufficient.

---

# 9️⃣ Presentation Files Missing

## ❗ Problem

`
presentation_outline.txt not found
`

## 🎯 Cause

Presentation script not executed after assessment.

## ✅ Solution

Run:

```bash
python3 scripts/presentation_summary.py
```

Verify:

```bash
ls -l reports/ | grep presentation
```

---

# 🔟 Survey Data Too Large or Slow

## ❗ Problem

Performance lag when processing survey responses.

## 🎯 Cause

Large dataset (thousands of responses).

## ✅ Solution

* Limit responses in generator:

  ```python
  generate_culture_survey(200)
  ```
* Optimize numpy mean calculations
* Consider pandas DataFrame for large-scale enterprise data

---

# 🧠 Best Practice Troubleshooting Approach

When something fails:

1. Confirm correct script order
2. Validate JSON integrity
3. Check installed modules
4. Verify directory structure
5. Confirm permissions
6. Re-run data generation
7. Inspect console logs carefully

---

# 🔐 Security Considerations

While troubleshooting:

* Do not expose real employee data
* Avoid storing sensitive production metrics in plain JSON
* Ensure deliverables folder permissions are restricted
* Use `.gitignore` to exclude generated data from version control

---

# 🎯 Final Validation Checklist

Before submitting:

✔ All scripts execute without error
✔ `assessment_results.json` generated
✔ Executive & detailed reports present
✔ Bar + radar charts generated
✔ Presentation files generated
✔ Deliverables ZIP created
✔ Directory structure matches expected layout

---

# 🏁 Conclusion

This troubleshooting guide ensures:

* Reliable execution of assessment framework
* Stable report generation
* Accurate maturity scoring
* Production-ready deliverables packaging

Following this structured approach guarantees smooth deployment in real-world environments.
