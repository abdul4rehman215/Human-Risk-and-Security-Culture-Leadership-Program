# 🛠 Troubleshooting Guide - Lab 3: Behavioral Science in Cybersecurity

---

# 🔎 Overview

This document outlines common issues encountered while implementing:

- `fogg_model.py`
- `risk_prioritization.py`
- `test_system.py`
- `org_assessment.py`

It also provides root causes and corrective actions.

---

# 1️⃣ Issue: Behavior Scores Always Return 0

## ❌ Symptoms

- All behavior scores display `0.0`
- Risk level always shows `High`
- Trend averages are incorrect

## 🔍 Root Cause

Possible causes:

- Inputs not normalized to 0–1 range
- Division by 10 missing
- Using addition instead of multiplication
- Negative values not clamped properly

## ✅ Solution

Verify:

```python
m = clamp_0_10(motivation) / 10.0
a = clamp_0_10(ability) / 10.0
t = clamp_0_10(trigger) / 10.0

score = (m * a * t) * 100.0
```

Ensure:

- Multiplication is used
- Clamping logic works
- Values are converted back to 0–100

---

# 2️⃣ Issue: Incorrect Risk Levels Assigned

## ❌ Symptoms

- High behavior score still marked "High Risk"
- Medium scores misclassified

## 🔍 Root Cause

Threshold logic implemented incorrectly.

## ✅ Correct Threshold Logic

```python
if behavior_score >= 70:
    likelihood = "High"
    risk_level = "Low"
elif behavior_score >= 40:
    likelihood = "Medium"
    risk_level = "Medium"
else:
    likelihood = "Low"
    risk_level = "High"
```

Important:  
High behavior score = LOW risk.

---

# 3️⃣ Issue: Risk Prioritization Does Not Match Expectations

## ❌ Symptoms

- Weak-user risks not ranked highest
- Priority scores unusually small or large

## 🔍 Root Cause

Incorrect behavioral risk factor calculation.

## ✅ Correct Formula

```
Priority Score = (Impact × Frequency × Behavioral_Risk_Factor) / 100

Behavioral_Risk_Factor = 100 - avg_behavior_score
```

Verify:

- Inversion is applied correctly
- Division by 100 is included
- All three factors are used

---

# 4️⃣ Issue: Risks Not Sorted Properly

## ❌ Symptoms

- Low priority appears above High/Critical
- List order inconsistent

## 🔍 Root Cause

Sorting not applied or incorrect sort direction.

## ✅ Fix

```python
self.prioritized_risks.sort(
    key=lambda x: x.get("priority_score", 0),
    reverse=True
)
```

Use `reverse=True` for descending order.

---

# 5️⃣ Issue: Recommendations Are Empty

## ❌ Symptoms

- No recommendations printed
- Empty list returned

## 🔍 Root Cause

Threshold condition not triggering.

## ✅ Check Conditions

```python
if avg_m < 5:
if avg_a < 5:
if avg_t < 5:
```

Ensure:

- Using `< 5`
- Values correctly cast to float
- Recommendations appended before return

Add fallback:

```python
if not recommendations:
    recommendations.append("Maintain current controls...")
```

---

# 6️⃣ Issue: JSON Export Fails

## ❌ Symptoms

- File not created
- Export function returns False
- JSON invalid

## 🔍 Root Cause

- Invalid file permissions
- Non-serializable object types
- File path incorrect

## ✅ Solution

Verify:

```bash
ls -lh
```

Ensure:

- Directory is writable
- Only JSON-serializable types used
- `datetime` converted to string using `.isoformat()`

---

# 7️⃣ Issue: Integration Test Fails

## ❌ Symptoms

- `[FAIL]` displayed during testing
- Overall result shows FAIL

## 🔍 Root Cause

One or more:

- Behavior score mismatch
- Risk ordering incorrect
- Missing priority_level field
- Export file not generated

## ✅ Debug Steps

1. Run each module individually:
   ```
   python3 fogg_model.py
   python3 risk_prioritization.py
   ```

2. Add debug prints inside:
   - calculate_behavior_score
   - calculate_risk_priority_score

3. Validate expected vs actual values.

---

# 8️⃣ Issue: Module Import Errors

## ❌ Symptoms

```
ModuleNotFoundError: No module named 'fogg_model'
```

## 🔍 Root Cause

Scripts not in same directory.

## ✅ Fix

Ensure directory structure:

```
fogg_cybersecurity_lab/
├── fogg_model.py
├── risk_prioritization.py
├── test_system.py
├── org_assessment.py
```

Run from project root:

```bash
cd ~/fogg_cybersecurity_lab
python3 test_system.py
```

---

# 9️⃣ Issue: Unexpected Low Organizational Scores

## ❌ Symptoms

- Departments marked "High Risk"
- Behavior scores seem low

## 🔍 Explanation

Multiplication model reduces overall score:

Example:

```
6 × 4 × 5 → 0.6 × 0.4 × 0.5 × 100 = 12
```

Even moderate weaknesses significantly lower overall behavior score.

This is expected and models real-world dependency.

---

# 🔟 Performance or Logical Errors

## Best Practices

- Use type hints consistently
- Use rounding for output display only
- Avoid mutating shared objects
- Validate test coverage after changes

---

# 🔐 Security-Relevant Notes

This lab demonstrates:

- Human vulnerability can outweigh technical controls
- High-value targets need behavioral reinforcement
- Weak triggers often undermine secure behavior
- Risk prioritization must incorporate human factors

Ignoring behavioral analysis leads to underestimating real-world cyber risk.

---

# 📌 Final Validation Checklist

Before pushing to GitHub:

✔ All scripts executable  
✔ No TODO placeholders remain  
✔ Tests pass with “Overall Result: PASS”  
✔ JSON files validate successfully  
✔ Output matches expected lab behavior  

---

# 🎯 Conclusion

Most implementation issues stem from:

- Incorrect normalization
- Wrong threshold logic
- Improper risk inversion
- Sorting errors

Once these are corrected, the system functions as designed.

This troubleshooting guide ensures smooth deployment and reproducibility of behavioral cybersecurity risk analysis.

