# 🧪 Lab 09: ADDIE Model for Training Development

## 🎯 Objectives

By the end of this lab, I was able to:

- Understand and apply the **five phases** of the ADDIE instructional design model
- Build a **Python framework** to manage training development workflows end-to-end
- Create structured training programs following **ADDIE methodology**
- Implement **assessment strategies** to measure training effectiveness
- Apply ADDIE principles to realistic security awareness training scenarios

---

## 📌 Prerequisites

- Basic Python programming (functions, dictionaries, file I/O)
- Familiarity with Linux command line
- Basic instructional design concepts
- Text editor experience (nano/vim/gedit)

---

## 🧰 Lab Environment

**Environment:** Ubuntu 24.04 (Cloud Lab Environment)  
**User:** `toor`
This lab was performed in a Linux cloud lab environment running **Ubuntu 24.04** with required tools pre-installed.

---

## 📚 ADDIE Model Summary

ADDIE is a systematic instructional design framework with five phases:

1. **Analyze** — Identify training needs and learner characteristics  
2. **Design** — Define learning objectives and assessment strategies  
3. **Develop** — Create training materials and content  
4. **Implement** — Deliver the training program  
5. **Evaluate** — Assess effectiveness and gather feedback  

This lab builds a Python-based management system that tracks each phase, generates artifacts, and produces final consolidated reports.

---

## 🧩 What I Built

✅ A complete **ADDIE management framework** in Python, including:

- `ADDIEFramework` base class for project tracking + persistence  
- Dedicated phase modules:
  - `analyze_phase.py`
  - `design_phase.py`
  - `develop_phase.py`
  - `implement_phase.py`
  - `evaluate_phase.py`
- A full orchestration runner:
  - `complete_addie_workflow.py` (runs full pipeline and generates final report)
- Data + reports generated automatically into phase directories

---

## 📁 Repo Structure (This Lab Folder)

```text
lab-09-addie-model/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
└── scripts/
    ├── addie_framework.py
    ├── analyze_phase.py
    ├── sample_analysis_data.py
    ├── design_phase.py
    ├── develop_phase.py
    ├── implement_phase.py
    ├── evaluate_phase.py
    └── complete_addie_workflow.py
````

> Note: During execution, the lab creates runtime artifacts under:
> `analyze/`, `design/`, `develop/`, `implement/`, `evaluate/`, `data/`, and `reports/`.

---

## ▶️ How to Run (Quick)

```bash
mkdir -p ~/addie_training_lab/{analyze,design,develop,implement,evaluate,scripts,data,reports}
cd ~/addie_training_lab

# after creating scripts...
chmod +x scripts/*.py

# run integrated workflow
./scripts/complete_addie_workflow.py
```

---

## ✅ Expected Outcomes

After completion, the workflow produced:

* Phase artifacts:

  * `analyze/*.json`
  * `design/*.json` + `.txt`
  * `develop/*.json` + `.txt`
  * `implement/*.json` + `.txt`
  * `evaluate/*.json` + `.txt`
* Project state file:

  * `data/Security_Awareness_Training_<timestamp>.json`
* Final consolidated report:

  * `reports/final_project_report_<timestamp>.txt`

---

## 🔐 Security / Real-World Relevance

Security awareness programs fail when content is not structured, measurable, or continuously improved.
This lab simulates an enterprise approach where:

* training design is **tracked**
* outcomes are **measured**
* improvement is **data-driven**
* artifacts are **auditable** (JSON + text reports)

This mirrors how security culture programs are built in real organizations.

---

## ✅ Conclusion

This lab provided hands-on experience implementing the **ADDIE model** as a fully automated Python workflow.
It reinforced the value of structured training development, documentation, and continuous evaluation — key for building scalable, measurable security awareness programs.

✅ **END OF LAB 09**
