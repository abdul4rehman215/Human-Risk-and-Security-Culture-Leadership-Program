mkdir -p ~/security-culture-lab/{data,scripts,templates,static/{css,js}}
cd ~/security-culture-lab
python3 -m venv venv
source venv/bin/activate
pip install flask pandas numpy matplotlib seaborn

nano scripts/setup_database.py
python scripts/setup_database.py
ls -lh data/security_culture.db

nano scripts/generate_sample_data.py
python scripts/generate_sample_data.py
sqlite3 data/security_culture.db "SELECT 'employees', COUNT(*) FROM employees; SELECT 'security_training', COUNT(*) FROM security_training; SELECT 'phishing_simulations', COUNT(*) FROM phishing_simulations; SELECT 'security_incidents', COUNT(*) FROM security_incidents; SELECT 'security_surveys', COUNT(*) FROM security_surveys;"

nano scripts/data_collector.py
nano scripts/culture_analyzer.py
nano scripts/trend_analyzer.py

python scripts/culture_analyzer.py
python scripts/trend_analyzer.py
ls -lh data/culture_report.json data/trend_report.json
python -c "import json; r=json.load(open('data/culture_report.json')); print('Avg training:', r['training_effectiveness']['average_score']); print('Click rate:', r['phishing_resilience']['click_rate']); print('Report rate:', r['phishing_resilience']['report_rate']); print('Culture score:', r['culture_score']['overall_culture_score']); print('Incidents:', r['incident_summary']['total_incidents'])"

nano scripts/dashboard_app.py
nano templates/dashboard.html
nano static/css/dashboard.css
nano static/js/dashboard.js

python scripts/dashboard_app.py

curl -s http://localhost:5000/api/culture-metrics | head
curl -s http://localhost:5000/api/trend-data | head
curl -s http://localhost:5000/api/department-metrics | head

python scripts/culture_analyzer.py
python scripts/trend_analyzer.py

ls -lh data/security_culture.db
chmod 644 data/security_culture.db
sudo apt update
sudo apt install -y sqlite3

sudo lsof -i :5000
pip list

curl -s http://localhost:5000/api/culture-metrics | head
curl -s http://localhost:5000/api/trend-data | head
curl -s http://localhost:5000/api/department-metrics | head

python scripts/generate_sample_data.py
