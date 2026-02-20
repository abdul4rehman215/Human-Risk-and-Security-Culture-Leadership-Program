## 🎤 Interview Q&A - Lab 15: Metrics for Measuring Security Culture

---

### 1) What do we mean by “security culture,” and why do we measure it?

**Answer:**
Security culture is the set of employee behaviors, beliefs, and habits that affect security outcomes (e.g., reporting phishing, following policy, completing training). We measure it to prove program effectiveness, identify weak areas (departments/roles), and take targeted action instead of guessing.

---

### 2) Why did we choose SQLite for this lab?

**Answer:**
SQLite is lightweight, requires no server, and is perfect for lab-scale structured data. It supports relational modeling (tables + foreign keys), which makes it ideal for joining employees with training, phishing, surveys, and incidents.

---

### 3) Explain the purpose of foreign keys in this database.

**Answer:**
Foreign keys maintain data integrity by linking records to valid employees. Example: `security_training.employee_id` references `employees.employee_id`, ensuring training rows always map to real people (or are handled safely if deleted). This prevents orphan data.

---

### 4) What are the core metric categories we tracked?

**Answer:**

* **Training effectiveness** (scores, completions, department averages)
* **Phishing resilience** (click rate, report rate, department breakdown)
* **Culture score** (awareness + behavior survey scores)
* **Incident summary** (incident types, severity, department patterns)

---

### 5) How did we calculate phishing click rate and report rate?

**Answer:**
We used the mean of binary fields:

* `clicked_link` mean × 100 = click rate (%)
* `reported_email` mean × 100 = report rate (%)
  This works because the values are stored as 0/1.

---

### 6) What does a “good” click rate and report rate look like?

**Answer:**
Generally:

* Click rate should trend **down**, ideally **below 10%** (varies by org maturity).
* Report rate should trend **up**, ideally **above 60%** or improving month-to-month.
  In the lab sample, click rate (~11.38%) was slightly high, and report rate (~53.27%) had room to improve.

---

### 7) How did we compute the overall culture score?

**Answer:**
We averaged survey-based **awareness_score** and **behavior_score** (both 1–10):
`overall = (awareness + behavior) / 2`
This provides a simple single indicator while still keeping awareness/behavior separate.

---

### 8) Why do we need trend analysis instead of only “current” metrics?

**Answer:**
A single snapshot can be misleading. Trend analysis shows whether the program is improving or declining over months (example: training scores improving, click rates decreasing). Trends help validate whether interventions are working.

---

### 9) Why did we build a Flask API instead of reading JSON directly in the browser?

**Answer:**
The Flask API dynamically generates fresh reports from the database and returns JSON consistently. This supports real-time dashboard updates and allows reuse of server-side logic (analysis + validation) without exposing DB access to the client.

---

### 10) What’s the value of D3.js in this dashboard?

**Answer:**
D3.js enables interactive visualizations (tooltips, grouped bars, lines, area charts) so stakeholders can quickly understand patterns and department differences. This makes security culture metrics easier to consume than raw tables.

---

### 11) Which department needed the most focus in the sample output, and why?

**Answer:**
**Sales** needed the most focus because it had:

* Highest click rate (~16.67%)
* Lowest culture score (~6.29/10)
  This suggests targeted anti-phishing coaching and reinforcement should be prioritized there.

---

### 12) If you were extending this lab for a real organization, what would you add?

**Answer:**

* Authentication for dashboard access
* Real ingestion pipeline (email gateway reports, LMS training exports, SIEM incidents)
* Alerts (e.g., if click rate rises above threshold)
* Role-based segmentation (executives vs staff)
* More detailed culture model (weights, confidence, response rates)

---

### 13) What are common pitfalls when measuring security culture?

**Answer:**

* Over-relying on training completion as “success”
* Not segmenting by department/role (hides weak areas)
* Poor survey design (bias, low response rate)
* Ignoring trends and seasonality
* Not converting metrics into actionable changes

---

### 14) How do we ensure the metrics are actionable?

**Answer:**
By mapping each metric to decisions:

* High click rate → targeted phishing training + more simulations
* Low reporting → reward/recognition + simpler reporting path
* Low training scores → refresh training content + micro-learning
* High incidents → improve controls, reinforce reporting and policy

---

## ✅ Next: Troubleshooting (Lab 15)

Type **next**.
