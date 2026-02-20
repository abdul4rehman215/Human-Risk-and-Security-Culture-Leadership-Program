# Lab 14 Commands

## Task 1: Designing the Ambassador Program Structure

### Step 1: Create folders + enter project
mkdir -p ~/ambassador_program/{surveys,analysis,training,reports}
cd ~/ambassador_program

### Create program framework document
nano program_framework.md

### Quick verify
sed -n '1,30p' program_framework.md

### Step 2: Create ambassador role description
nano ambassador_role.md

### Quick verify
head -n 25 ambassador_role.md

## Task 2: Creating Assessment Surveys

### Step 1: Create survey questions JSON
cd ~/ambassador_program/surveys
nano survey_questions.json

### Validate JSON format
python3 -m json.tool survey_questions.json > /dev/null
echo $?

### Step 2: Create survey deployment guide
nano survey_deployment_guide.md

### Quick verify
tail -n 12 survey_deployment_guide.md

## Task 3: Survey Data Analysis with Python

### Step 1: Setup Python environment
cd ~/ambassador_program
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

### Install dependencies
pip install pandas numpy matplotlib

### Create analyzer script
cd ~/ambassador_program/analysis
nano survey_analyzer.py

### Run analyzer (sample mode)
python3 survey_analyzer.py

### Verify outputs
ls -lh analysis_report.txt plots/*.png

### Quick peek into report
head -n 28 analysis_report.txt

### Step 2: Create program tracker script
nano program_tracker.py

### Run tracker
python3 program_tracker.py

### Verify tracker outputs
ls -lh tracking_charts/program_dashboard.png exports/ambassadors.csv exports/activities.csv exports/metrics.json

### View metrics.json
cat exports/metrics.json

## Task 4: Developing Training Materials

### Step 1: Create training curriculum
cd ~/ambassador_program/training
nano training_curriculum.md

### Step 2: Create training resources
nano training_resources.md

### Step 3: Create assessment template
nano ambassador_assessment.json

### Validate JSON
python3 -m json.tool ambassador_assessment.json > /dev/null
echo $?

## Task 5: Establishing Program Metrics

### Step 1: Create KPI document
cd ~/ambassador_program/reports
nano program_metrics.md

### Step 2: Create quarterly report template
nano quarterly_report_template.md

### Step 3: Create metrics dashboard script
cd ~/ambassador_program/analysis
nano metrics_dashboard.py

### Run metrics dashboard script
python3 metrics_dashboard.py

### Verify dashboard + executive summary
ls -lh metrics_charts/metrics_dashboard.png exports/executive_summary.txt

### View executive summary
cat exports/executive_summary.txt
