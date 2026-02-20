#!/usr/bin/env python3
"""
Package all assessment deliverables
Full Implementation (All TODOs completed)
"""

import shutil
from pathlib import Path
from datetime import datetime


def package_deliverables():
    """
    Create final deliverables package
    - deliverables/<timestamp>/reports/
    - deliverables/<timestamp>/scripts/
    - deliverables/<timestamp>/data/
    - README.txt
    - optional zip archive
    """
    base_dir = Path.cwd()
    reports_dir = base_dir / "reports"
    data_dir = base_dir / "data"
    scripts_dir = base_dir / "scripts"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    deliverables_root = base_dir / "deliverables" / f"security_culture_assessment_{timestamp}"

    # Create directory structure
    (deliverables_root / "reports").mkdir(parents=True, exist_ok=True)
    (deliverables_root / "data").mkdir(parents=True, exist_ok=True)
    (deliverables_root / "scripts").mkdir(parents=True, exist_ok=True)

    # Copy reports
    if reports_dir.exists():
        for f in reports_dir.glob("*"):
            if f.is_file():
                shutil.copy2(f, deliverables_root / "reports" / f.name)

    # Copy data
    if data_dir.exists():
        for f in data_dir.glob("*.json"):
            if f.is_file():
                shutil.copy2(f, deliverables_root / "data" / f.name)

    # Copy scripts
    if scripts_dir.exists():
        for f in scripts_dir.glob("*.py"):
            if f.is_file():
                shutil.copy2(f, deliverables_root / "scripts" / f.name)

    # Create README
    readme_path = deliverables_root / "README.txt"
    readme = f"""
SECURITY CULTURE ASSESSMENT - DELIVERABLES PACKAGE
==================================================
Package Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CONTENTS
--------
reports/
  - assessment_results.json          : Final assessment output (scores, maturity, recommendations)
  - executive_summary.txt            : Executive-level summary report
  - detailed_report.txt              : Full detailed report
  - maturity_scores.png              : Bar chart of category maturity scores
  - maturity_radar.png               : Radar chart of category scores
  - presentation_outline.txt         : Slide outline for stakeholder presentation
  - presentation_talking_points.txt  : Speaker notes/talking points

data/
  - training_metrics.json            : Sample training metrics
  - phishing_metrics.json            : Sample phishing simulation metrics
  - incident_metrics.json            : Sample incident metrics
  - survey_responses.json            : Sample culture survey responses

scripts/
  - config.py                        : Weights, thresholds, and configuration
  - generate_data.py                 : Data generator
  - assessment_analyzer.py           : Assessment engine
  - report_generator.py              : Report + chart generator
  - presentation_summary.py          : Presentation materials generator
  - package_deliverables.py          : Packaging utility

HOW TO RE-RUN
-------------
1) Generate data:
   python3 scripts/generate_data.py

2) Run assessment:
   python3 scripts/assessment_analyzer.py

3) Generate reports:
   python3 scripts/report_generator.py

4) Generate presentation materials:
   python3 scripts/presentation_summary.py
""".strip() + "\n"

    with open(readme_path, "w") as f:
        f.write(readme)

    print(f"[+] Deliverables folder created: {deliverables_root}")

    # Create optional archive (zip)
    archive_base = base_dir / "deliverables" / f"security_culture_assessment_{timestamp}"
    shutil.make_archive(str(archive_base), "zip", root_dir=deliverables_root)

    print(f"[+] ZIP archive created: {archive_base}.zip")
    print("Deliverables packaged successfully")


if __name__ == "__main__":
    package_deliverables()
