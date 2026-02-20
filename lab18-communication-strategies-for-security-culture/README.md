# 🔐 Lab 18: Communication Strategies for Security Culture (Golden Circle + Automation)

## 📌 Lab Overview
This lab builds a **scalable security culture communication system** using the **Golden Circle model (Why → How → What)** and automated workflows. The outcome is a **multi-audience messaging framework**, **communication plan generator**, **simulated email sender**, **scheduler**, **engagement metrics tracker**, and a **text-based dashboard** for ongoing awareness campaigns.

---

## 🎯 Objectives
By the end of this lab, I was able to:

- ✅ Apply the **Golden Circle framework (Why–How–What)** to security culture messaging
- ✅ Create **targeted messages** for Executives, Managers, and Employees
- ✅ Implement **automated communication workflows** using Python
- ✅ Build a **communication plan** with scheduling and measurable success metrics
- ✅ Track engagement using **JSON-based metrics**
- ✅ Generate a **dashboard** to monitor campaign performance

---

## ✅ Prerequisites
- Basic Python programming
- Familiarity with Linux CLI
- Understanding of security culture and stakeholder communication
- Basic knowledge of JSON structures

---

## 🧪 Lab Environment
- OS: Ubuntu 22.04 (Cloud Lab)
- Python: 3.10+
- Editor: nano
- Prompt: `student@ip-172-31-14-221:~$`

---

## 🗂️ Repository Structure

```text
lab18-communication-strategies-for-security-culture/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
│
├── data/
│   ├── communication_plan.json
│   ├── communication_metrics.json
│   ├── email_config.json
│   ├── email_schedule.json
│   ├── executive_message.txt
│   └── employee_message.txt
│
├── golden-circle/
│   └── security_golden_circle.py
│
├── logs/
│   └── email_log.json
│
├── scripts/
│   ├── communication_dashboard.py
│   ├── communication_metrics.py
│   ├── email_config.py
│   ├── email_scheduler.py
│   └── email_templates.py
│
└── templates/
    ├── communication_plan.py
    ├── sample_executive.html
    ├── sample_manager.html
    └── sample_employee.html
```

---

## 🧱 What I Built

### 1) 🟡 Golden Circle Messaging Engine

**File:** `golden-circle/security_golden_circle.py`

* Stores **WHY / HOW / WHAT** statements
* Generates:

  * `data/executive_message.txt` (ROI + risk framing)
  * `data/employee_message.txt` (practical relevance + actions)

✅ Output confirmed with message preview + file creation.

---

### 2) 📅 Communication Plan Generator (JSON)

**File:** `templates/communication_plan.py`

Generates a structured plan containing:

* Target audiences + characteristics
* Channels + frequency
* 12-month messaging calendar
* Success metrics (open rate, phishing rate, training completion, incident reporting)

✅ Saved as: `data/communication_plan.json`

---

### 3) 📧 Email Automation System (Simulated)

Since this is a lab environment, SMTP sending is simulated to avoid real outbound mail dependency.

#### a) Email Config + Sender (Simulated Send + Logging)

**File:** `scripts/email_config.py`

* Creates default config in `data/email_config.json` if missing
* Simulates sending to sample recipients
* Writes a JSON log to `logs/email_log.json`

#### b) Audience-Specific Email Templates (Golden Circle-Aligned HTML)

**File:** `scripts/email_templates.py`

* Executive template: **ROI + risk + compliance**
* Manager template: **team toolkit + actions**
* Employee template: **weekly tips + training CTA**
* Saves samples:

  * `templates/sample_executive.html`
  * `templates/sample_manager.html`
  * `templates/sample_employee.html`

#### c) Email Scheduler (Monthly/Bi-weekly/Weekly)

**File:** `scripts/email_scheduler.py`
Creates a 12-month schedule:

* Executives: **12**
* Managers: **24**
* Employees: **48**
  Total scheduled: **84 emails**

✅ Saved schedule: `data/email_schedule.json`
✅ Logged sends: `logs/email_log.json`

---

### 4) 📊 Metrics + Dashboard

#### a) Communication Metrics Tracker

**File:** `scripts/communication_metrics.py`
Tracks:

* sent / opened / clicked totals
* breakdown by audience
* monthly breakdown
* engagement rate calculation

✅ Saved metrics: `data/communication_metrics.json`

#### b) Text-Based Dashboard (Ops-Friendly)

**File:** `scripts/communication_dashboard.py`
Displays:

* totals + engagement
* upcoming scheduled emails
* audience breakdown
* monthly trends
* recommendations based on engagement

✅ Outputs a clear snapshot without needing a GUI.

---

## ▶️ How to Run (Quick Start)

### 1) Create project folders

```bash
mkdir -p ~/security-communication-lab/{golden-circle,templates,scripts,logs,data}
cd ~/security-communication-lab
tree -d
```

### 2) Run Golden Circle messages

```bash
chmod +x golden-circle/security_golden_circle.py
python3 golden-circle/security_golden_circle.py
ls -la data/
```

### 3) Generate communication plan

```bash
python3 templates/communication_plan.py
ls -la data/
```

### 4) Test simulated email sender

```bash
chmod +x scripts/email_config.py
python3 scripts/email_config.py
ls -la logs/
```

### 5) Generate template samples

```bash
chmod +x scripts/email_templates.py
python3 scripts/email_templates.py
ls -la templates/
```

### 6) Build + run scheduler

```bash
chmod +x scripts/email_scheduler.py
cd scripts
python3 email_scheduler.py
cd ..
ls -la data/ logs/
```

### 7) Generate metrics + dashboard

```bash
chmod +x scripts/communication_metrics.py scripts/communication_dashboard.py
python3 scripts/communication_metrics.py
python3 scripts/communication_dashboard.py
```

---

## ✅ Results (Observed)

* 📌 **84 scheduled communications**
* 📌 Metrics simulation produced:

  * **Overall engagement**: 88.75%
  * Executives engagement: 120% (opens+clicks can exceed sent in this demo model)
  * Managers engagement: 100%
  * Employees engagement: 83.33%
* 📌 Full logs and JSON tracking created successfully

---

## 💼 Why This Matters (Real-World Relevance)

Security culture doesn’t scale through ad-hoc reminders. This lab demonstrates how to:

* communicate security with **stakeholder-specific value framing**
* automate consistent messaging without heavy manual effort
* track adoption using **measurable engagement signals**
* adapt strategy using a feedback loop (metrics → dashboard → recommendations)

---

## 🧠 Key Takeaways

* Golden Circle improves persuasion by anchoring messages in **purpose and impact**
* Segmentation is required: **Executives want ROI, employees want relevance**
* Automation enables reliability: **campaigns fail when consistency fails**
* Metrics make programs defensible: **what gets measured gets improved**

---

## 🏁 Conclusion

This lab delivered a complete foundation for **security culture communication at scale**:

* Golden Circle messaging engine ✅
* Audience-specific templates ✅
* Automated scheduling system ✅
* Engagement metrics + dashboard ✅

This structure can be extended to integrate real SMTP, Slack/Teams, LMS APIs, or security platform signals (SIEM/SOAR) for end-to-end culture operations.
