## Lab 16 — `commands.sh`

```bash
#!/bin/bash
# Lab 16 - ROI of Security Culture Programs
# Commands Executed During Lab (sequential, paste-ready)

# ---------------------------
# Task 1: Environment Setup
# ---------------------------

mkdir -p ~/security_roi_lab/{data,scripts,reports,visualizations}
cd ~/security_roi_lab

python3 -m venv security_roi_env
source security_roi_env/bin/activate

pip install pandas numpy matplotlib seaborn plotly
pip install dash

# Optional headless fix (Ubuntu 24.04 cloud labs)
export MPLBACKEND=Agg
echo $MPLBACKEND

# Confirm structure
ls -la

# ---------------------------
# Task 1.3: Generate Sample Data
# ---------------------------

nano scripts/data_generator.py
chmod +x scripts/data_generator.py

cd ~/security_roi_lab/scripts
python3 data_generator.py

ls -lh ../data/security_metrics.csv
head -n 5 ../data/security_metrics.csv

# ---------------------------
# Task 2: ROI Calculation Model
# ---------------------------

nano roi_calculator.py
chmod +x roi_calculator.py

python3 roi_calculator.py

ls -lh ../reports/
cat ../reports/roi_summary.json

# ---------------------------
# Task 3: Static Visualizations
# ---------------------------

nano visualization.py
chmod +x visualization.py

python3 visualization.py
ls -lh ../visualizations/

# ---------------------------
# Task 4: Interactive Dashboard (Optional)
# ---------------------------

nano interactive_dashboard.py
chmod +x interactive_dashboard.py

python3 interactive_dashboard.py

# ---------------------------
# Troubleshooting Checks Used
# ---------------------------

export MPLBACKEND=Agg
sudo netstat -tuln | grep 8050
pip list | grep -E "dash|plotly"
```
