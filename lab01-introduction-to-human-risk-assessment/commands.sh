# ================================
# Lab 1 — Commands Executed
# Introduction to Human Risk Assessment
# OS: Ubuntu 24.04
# User: toor
# ================================

# ---- Task 1.1: Create Project Structure ----
mkdir -p ~/human-risk-assessment/{framework,data,surveys,reports,scripts}
cd ~/human-risk-assessment

touch framework/risk-framework.md
touch framework/risk-indicators.txt
touch data/assessment-data.csv

ls -R

# ---- Task 1.2: Create Risk Framework ----
nano framework/risk-framework.md
sed -n '1,120p' framework/risk-framework.md

# ---- Task 1.3: Install Required Tools + Python venv ----
sudo apt update
sudo apt install -y python3 python3-pip python3-venv sqlite3 acl

cd ~/human-risk-assessment
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pandas matplotlib seaborn numpy

# (Reminder command used later whenever running scripts)
source ~/human-risk-assessment/.venv/bin/activate

# ---- Task 1.4: Create SQLite Database (interactive) ----
cd ~/human-risk-assessment/data
sqlite3 assessment.db
echo "Database created successfully"
ls -lh ~/human-risk-assessment/data/assessment.db

# ---- Task 2.1: Risk Indicators List ----
nano ~/human-risk-assessment/framework/risk-indicators.txt
head -n 60 ~/human-risk-assessment/framework/risk-indicators.txt

# ---- Task 2.2: Risk Scoring Script ----
nano ~/human-risk-assessment/scripts/risk_scoring.py
chmod +x ~/human-risk-assessment/scripts/risk_scoring.py
ls -lh ~/human-risk-assessment/scripts/risk_scoring.py

# ---- Task 2.3: Dashboard Script ----
nano ~/human-risk-assessment/scripts/risk_dashboard.py
chmod +x ~/human-risk-assessment/scripts/risk_dashboard.py
ls -lh ~/human-risk-assessment/scripts/risk_dashboard.py

# ---- Task 3.1: Install & Configure Apache/PHP + SQLite extension ----
sudo apt install -y apache2 php libapache2-mod-php php-sqlite3
sudo systemctl start apache2
sudo systemctl enable apache2

sudo mkdir -p /var/www/html/risk-survey
sudo chown -R $USER:$USER /var/www/html/risk-survey

systemctl is-active apache2

# ---- Task 3.2: Create Survey Form ----
nano /var/www/html/risk-survey/index.html
ls -lh /var/www/html/risk-survey/index.html

# ---- Task 3.3: Create Survey Processing Script ----
nano /var/www/html/risk-survey/process_survey.php
ls -lh /var/www/html/risk-survey/process_survey.php

# ---- Task 3.4: Permissions + Test ----
sudo chown -R www-data:www-data /var/www/html/risk-survey
sudo chmod -R 755 /var/www/html/risk-survey
ls -ld /var/www/html/risk-survey

sudo chown www-data:www-data ~/human-risk-assessment/data/assessment.db
sudo chmod 664 ~/human-risk-assessment/data/assessment.db

sudo chmod o+x ~
sudo chmod o+x ~/human-risk-assessment
sudo chmod o+x ~/human-risk-assessment/data

namei -l ~/human-risk-assessment/data/assessment.db

echo "Survey available at: http://localhost/risk-survey/"
curl -I http://localhost/risk-survey/
curl -I http://localhost/risk-survey/process_survey.php

# ---- Task 4.1: Generate Sample Data ----
nano ~/human-risk-assessment/scripts/generate_sample_data.py
chmod +x ~/human-risk-assessment/scripts/generate_sample_data.py
ls -lh ~/human-risk-assessment/scripts/generate_sample_data.py

cd ~/human-risk-assessment
source .venv/bin/activate

cd ~/human-risk-assessment/scripts
python3 generate_sample_data.py

sqlite3 ../data/assessment.db "SELECT COUNT(*) FROM participants;"
sqlite3 ../data/assessment.db "SELECT COUNT(*) FROM risk_responses;"

# ---- Task 4.2: Analyze Data + Generate Reports ----
nano ~/human-risk-assessment/scripts/analyze_data.py
chmod +x ~/human-risk-assessment/scripts/analyze_data.py
ls -lh ~/human-risk-assessment/scripts/analyze_data.py

cd ~/human-risk-assessment
source .venv/bin/activate

cd ~/human-risk-assessment/scripts
python3 analyze_data.py

sqlite3 ../data/assessment.db "SELECT COUNT(*) FROM risk_scores;"

# ---- Task 4.3: View Results ----
cat ~/human-risk-assessment/reports/summary_report.md
ls -lh ~/human-risk-assessment/reports/

sqlite3 ~/human-risk-assessment/data/assessment.db
