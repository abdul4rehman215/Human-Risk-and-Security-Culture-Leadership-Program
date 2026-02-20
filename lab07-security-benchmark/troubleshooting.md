# 🛠️ Troubleshooting Guide - Lab 7: Benchmarking Your Security Program

---

# 1️⃣ YAML Parsing Errors

## Problem
`
yaml.scanner.ScannerError: mapping values are not allowed here
`

## Cause
- Incorrect indentation (YAML requires spaces, not tabs)
- Missing colon
- Improper list formatting

## Solution

Validate YAML quickly:

```bash
python3 -c "import yaml; print(yaml.safe_load(open('data/sample_responses.yaml')))"
````

Expected output:

```
{'organization': {'name': 'TechCorp Inc', 'industry': 'Technology', 'date': '2024-01-15'}, 'responses': {...}}
```

Fixes:

* Use **spaces only**
* Ensure consistent indentation (2 spaces recommended)
* Check list format:

```
governance: [3, 4]
```

---

# 2️⃣ Module Import Errors

## Problem

`
ModuleNotFoundError: No module named 'benchmark_analyzer'
`

## Cause

Script executed from wrong directory.

## Solution

Always run from project root:

```bash
cd ~/security-benchmark
source venv/bin/activate
python3 scripts/run_benchmark.py data/sample_responses.yaml
```

---

# 3️⃣ Virtual Environment Not Activated

## Problem

`
ModuleNotFoundError: No module named 'pandas'
`

## Cause

venv not activated.

## Solution

```bash
source venv/bin/activate
```

Confirm:

```
(venv) toor@...
```

---

# 4️⃣ Response Count Mismatch Error

## Problem

`
ValueError: Response count mismatch for domain 'governance'
`

## Cause

Number of answers does not match number of questions.

Example:

```
governance:
  - question: ...
  - question: ...
```

Requires:

```
governance: [x, y]
```

## Solution

Ensure equal count of responses per domain.

---

# 5️⃣ Division by Zero

## Problem

Unexpected 0 overall score.

## Cause

* Domain weight missing
* Question weight = 0

## Fix

Check `framework.yaml`:

```
domains:
  governance:
    weight: 0.25
```

Check `questions.yaml`:

```
weight: 0.4
```

---

# 6️⃣ Matplotlib Chart Not Displaying

## Problem

`xdg-open` does nothing.

## Cause

Cloud lab is headless (no GUI).

## Solution

Charts are saved as PNG:

```
reports/domain_scores.png
reports/assessment_trend.png
```

Download file locally or view via:

```bash
ls reports/
```

---

# 7️⃣ Permission Errors

## Problem

`
Permission denied
`

## Cause

Script not executable.

## Solution

```bash
chmod +x scripts/*.py
```

---

# 8️⃣ Incorrect Overall Score

## Expected From Sample Data

| Domain             | Score |
| ------------------ | ----- |
| governance         | 72%   |
| risk_management    | 50%   |
| incident_response  | 52%   |
| awareness          | 74%   |
| technical_controls | 68%   |

Overall:

```
63.9%
```

If different:

* Check weights
* Check normalization logic
* Verify YAML content

---

# 9️⃣ Trend Comparison Not Working

## Problem

`
Usage: python3 scripts/compare_assessments.py ...
`

## Cause

No file arguments provided.

## Correct Usage

```bash
python3 scripts/compare_assessments.py data/sample_responses.yaml data/sample_responses.yaml
```

---

# 🔟 Corrupted YAML Output File

If interactive YAML file appears broken:

Delete and rerun:

```bash
rm data/interactive_responses_*.yaml
python3 scripts/interactive_assessment.py
```

---

# 1️⃣1️⃣ Seaborn Styling Errors

If style error occurs:

```bash
pip install --upgrade seaborn
```

---

# 1️⃣2️⃣ Verify Environment

Check Python version:

```bash
python3 --version
```

Expected:

```
Python 3.12.x
```

Check installed packages:

```bash
pip list
```

---

# ✅ Recommended Clean Execution Order

```bash
cd ~/security-benchmark
source venv/bin/activate

python3 scripts/run_benchmark.py data/sample_responses.yaml
python3 scripts/interactive_assessment.py
python3 scripts/compare_assessments.py data/sample_responses.yaml data/sample_responses.yaml
```

---

# 🔍 Validation Checklist

✔ framework.yaml loads successfully
✔ questions.yaml properly formatted
✔ sample_responses.yaml valid
✔ Domain scores calculated
✔ Overall score = 63.9%
✔ assessment_report.md generated
✔ domain_scores.png generated
✔ assessment_trend.png generated

---

# 🧠 Debug Strategy

If something fails:

1. Validate YAML
2. Check virtual environment
3. Confirm working directory
4. Verify file paths
5. Re-run scripts sequentially
6. Print debug values in analyzer if needed

---

# 🎯 Final Notes

Common mistakes in this lab:

* Running script from wrong directory
* YAML indentation errors
* Forgetting to activate venv
* Editing framework without updating questions
* Response mismatch errors

Always validate configuration files before executing scoring logic.

---

End of Troubleshooting Guide
Lab 7 – Benchmarking Your Security Program
