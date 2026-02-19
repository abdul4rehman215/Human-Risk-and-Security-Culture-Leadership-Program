# 🛠️ Troubleshooting Guide — Lab 04: Security Awareness Maturity Model (SAMM)

This guide lists common issues encountered during the lab and how to resolve them in a cloud Ubuntu 24.04 environment.

---

## 1) Module import errors (config not found / samm_config import fails)

### ✅ Symptoms
- `ModuleNotFoundError: No module named 'samm_config'`
- Import failures when running `samm_engine.py`

### 🔍 Cause
- Script is executed from the wrong directory, or the config path is not added properly.
- Missing `scripts/__init__.py` or incorrect `sys.path` modification.

### ✅ Resolution
- Run scripts from the `scripts/` directory as shown in lab instructions:
```bash
cd ~/samm-lab/scripts
python3 samm_engine.py ../data/sample_survey_data.csv
````

* Verify `scripts/__init__.py` exists:

```bash
ls -l ~/samm-lab/scripts/__init__.py
```

* Confirm the config path line exists in `samm_engine.py`:

```python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))
```

---

## 2) Missing data / empty results

### ✅ Symptoms

* Assessment says: `No responses found in survey file.`
* Data analyzer fails due to missing columns
* CSV file appears empty or malformed

### 🔍 Cause

* Data generator script not run or wrote to an unexpected path
* CSV file does not include required columns
* File path passed to script is wrong

### ✅ Resolution

* Confirm the dataset exists:

```bash
ls -lh ~/samm-lab/data/sample_survey_data.csv
```

* Preview header and first rows:

```bash
head -n 5 ~/samm-lab/data/sample_survey_data.csv
```

* Re-run generator:

```bash
cd ~/samm-lab/scripts
python3 generate_sample_data.py
```

---

## 3) CSV parsing issues (unexpected column types)

### ✅ Symptoms

* `ValueError` related to conversion
* Some fields appear as strings instead of numeric values

### 🔍 Cause

* CSV may contain whitespace, missing values, or corrupted rows.
* Type conversion logic may treat unexpected values as strings.

### ✅ Resolution

* Validate the CSV structure:

```bash
python3 -c "import pandas as pd; df=pd.read_csv('~/samm-lab/data/sample_survey_data.csv'); print(df.dtypes); print(df.head())"
```

* Regenerate clean data:

```bash
cd ~/samm-lab/scripts
python3 generate_sample_data.py
```

---

## 4) Visualization errors in headless environment

### ✅ Symptoms

* Matplotlib errors such as backend issues
* `cannot connect to X server`
* Plots not generated or missing PNG files

### 🔍 Cause

* Running in cloud environments without a GUI backend.
* Missing backend configuration.

### ✅ Resolution

* Ensure `Agg` backend is set (already included in this lab):

```python
plt.switch_backend("Agg")
```

* Ensure output directory exists:

```bash
mkdir -p ~/samm-lab/reports
```

* Re-run analyzer:

```bash
cd ~/samm-lab/scripts
python3 data_analyzer.py ../data/sample_survey_data.csv ../reports
```

---

## 5) Report generation works but HTML images do not appear

### ✅ Symptoms

* HTML report opens but charts are missing
* Browser shows broken image icons

### 🔍 Cause

* HTML expects PNG files to be in the same directory as HTML.
* The analysis module generated plots elsewhere, or filenames do not match.

### ✅ Resolution

* Ensure plots exist in the same directory as the HTML file:

```bash
ls -lh ~/samm-lab/reports/*.png
```

* If plots are elsewhere, copy them into `reports/`:

```bash
cp /path/to/plots/*.png ~/samm-lab/reports/
```

* Re-run the report generator after confirming charts exist:

```bash
cd ~/samm-lab/scripts
python3 report_generator.py ../reports/samm_results.json ../reports/analysis_results.json
```

---

## 6) Incorrect maturity level calculations

### ✅ Symptoms

* Scores look correct but maturity levels are unexpectedly low/high
* Weighted score does not match expectation

### 🔍 Cause

* Threshold mapping is misconfigured
* Category weights do not sum to 1.0 (or are incorrect)
* Missing subcategories reduce average scores

### ✅ Resolution

* Verify thresholds in config:

```bash
cat ~/samm-lab/config/samm_config.py | sed -n '1,200p'
```

* Confirm weights sum to 1.0:

  * Governance (0.25) + Training (0.30) + Culture (0.25) + Measurement (0.20) = **1.00**

* Confirm each category’s subcategories exist and match CSV column names:

  * Example column format:

    * `training_role_based_training`
    * `culture_peer_influence`

---

## 7) Permission errors when saving reports or plots

### ✅ Symptoms

* `PermissionError: [Errno 13] Permission denied`
* JSON/PNG files not created

### 🔍 Cause

* Running scripts in a directory without write permissions
* Output directory not created

### ✅ Resolution

* Use the lab directory in your home folder:

```bash
cd ~/samm-lab/scripts
```

* Ensure output directory exists:

```bash
mkdir -p ~/samm-lab/reports
```

* Verify permissions:

```bash
ls -ld ~/samm-lab ~/samm-lab/reports
```

---

## ✅ Quick Verification Checklist

Run these checks if something looks wrong:

```bash
cd ~/samm-lab
tree -L 2

ls -lh data/sample_survey_data.csv
ls -lh reports/

cd scripts
python3 samm_engine.py ../data/sample_survey_data.csv
python3 data_analyzer.py ../data/sample_survey_data.csv ../reports
python3 report_generator.py ../reports/samm_results.json ../reports/analysis_results.json
```

If all commands run successfully, your SAMM pipeline is working end-to-end.
