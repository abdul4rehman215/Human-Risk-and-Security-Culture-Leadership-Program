# 🛠 Troubleshooting Guide - Lab 14: Building Ambassador Programs

---

## 🔹 Issue 1: Low Survey Response Rate

### Symptoms
- Few responses received
- Certain departments not represented
- Incomplete survey data

### Possible Causes
- Survey too long
- Lack of leadership endorsement
- Poor communication
- Employees unsure about confidentiality

### Solutions
- Keep survey under 10 minutes
- Send personalized reminder emails
- Have leadership promote participation
- Clearly state confidentiality policy
- Offer small participation incentives
- Send reminder after 7 days

---

## 🔹 Issue 2: JSON Validation Fails

### Symptoms
`
python3 -m json.tool survey_questions.json
`

Returns error instead of `0`.

### Possible Causes

* Missing comma
* Extra trailing comma
* Incorrect quotes
* Improper bracket closure

### Solutions

* Check for trailing commas
* Validate using `python3 -m json.tool`
* Use proper double quotes `" "` for JSON
* Ensure all `{}` and `[]` are properly closed

---

## 🔹 Issue 3: Python Virtual Environment Issues

### Symptoms

* `ModuleNotFoundError`
* `pip install` fails
* Wrong Python version detected

### Solutions

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pandas numpy matplotlib
```

* Ensure `(venv)` appears in terminal
* Verify Python version with:

```bash
python3 --version
```

---

## 🔹 Issue 4: survey_analyzer.py Fails to Load Data

### Error Example

`
FileNotFoundError: Survey file not found
`

### Possible Causes

* Incorrect file path
* Wrong working directory
* Missing CSV/Excel file

### Solutions

* Use absolute paths
* Confirm file exists with:

```bash
ls -lh
```

* Ensure CSV column names match expected structure

Required columns:

* department
* years_with_org
* security_knowledge
* topics_confident
* help_frequency
* presentation_comfort
* ambassador_interest
* time_available
* motivation_text

---

## 🔹 Issue 5: No Candidates Identified

### Symptoms

* `identify_candidates()` returns empty result

### Possible Causes

* Minimum score threshold too high
* Low interest or knowledge ratings

### Solutions

* Lower threshold:

```python
identify_candidates(min_score=3.0)
```

* Consider potential over current expertise
* Add training support for motivated candidates

---

## 🔹 Issue 6: program_tracker.py Not Generating Dashboard

### Symptoms

* No `tracking_charts/` directory created
* No PNG file generated

### Possible Causes

* No activities logged
* Matplotlib not installed
* Permission issues

### Solutions

* Ensure activities were logged before generating dashboard
* Install matplotlib:

```bash
pip install matplotlib
```

* Check write permissions:

```bash
ls -ld tracking_charts
```

---

## 🔹 Issue 7: metrics_dashboard.py Cannot Find Metrics File

### Error

`
FileNotFoundError: No metrics found.
`
### Causes

* `program_tracker.py` not executed
* `exports/metrics.json` missing

### Fix

Run:

```bash
python3 program_tracker.py
```

Then rerun:

```bash
python3 metrics_dashboard.py
```

---

## 🔹 Issue 8: Impact Score Seems Too Low

### Explanation

Impact score is normalized and capped:

* Activity volume (40%)
* Reach (40%)
* Growth trend (20%)

Low values may indicate:

* Limited activities
* Small reach
* No month-over-month growth

### Recommendation

* Increase activity volume
* Expand department coverage
* Encourage ambassadors to conduct more sessions

---

## 🔹 Issue 9: Ambassador Engagement Drops Over Time

### Indicators

* Declining activity count
* Reduced attendance
* Fewer logged activities

### Mitigation Strategies

* Recognize ambassadors publicly
* Offer quarterly incentives
* Refresh training materials
* Create ambassador peer network
* Schedule quarterly strategy meetings

---

## 🔹 Issue 10: Dashboard Charts Appear Blank

### Causes

* No data available
* Empty monthly trends
* Incorrect metrics format

### Solution

* Verify `metrics.json` contains:

  * total_ambassadors
  * total_activities
  * total_people_reached
  * monthly_trends
* Re-run tracker before dashboard

---

# ✅ Final Troubleshooting Checklist

✔ Virtual environment activated
✔ Required Python libraries installed
✔ JSON validated
✔ CSV structure correct
✔ Activities logged before generating metrics
✔ Correct file paths used
✔ Proper permissions on export folders

---

## 🎯 Key Takeaway

Most issues stem from:

* Incorrect file paths
* Missing dependencies
* Data format mismatches
* Running scripts in the wrong order

Following proper execution sequence resolves 95% of problems.

---
