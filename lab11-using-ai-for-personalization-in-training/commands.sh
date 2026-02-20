#!/bin/bash
# Lab 11 - Using AI for Personalization in Training
# Commands Executed During Lab

# -------------------------------
# Task 1: Set Up Development Environment
# -------------------------------

mkdir -p ~/ai-training-lab/{src,data,audio,templates,output}
cd ~/ai-training-lab

ls -1

python3 -m venv venv
source venv/bin/activate

python --version

pip install openai python-dotenv flask pyttsx3 gtts

pip freeze > requirements.txt
wc -l requirements.txt

nano .env
cat .env

# -------------------------------
# Task 2: Implement User Profile Management
# -------------------------------

nano src/user_profile.py
ls -l src/user_profile.py

nano test_profiles.py
python test_profiles.py

ls -lh data/profiles.json

# -------------------------------
# Task 3: Build AI Content Generator
# -------------------------------

nano src/content_generator.py
python -c "from src.content_generator import AIContentGenerator; g=AIContentGenerator(); print('demo_mode:', g.demo_mode, 'model:', g.model)"

nano src/training_manager.py

nano test_content.py
python test_content.py

ls -lh data/training_sessions.json
python -c "import json; d=json.load(open('data/training_sessions.json')); print('sessions:',len(d)); print('keys:',sorted(d[0].keys())); print('lesson_id:',d[0]['lesson_id']);"
python -c "import json; d=json.load(open('data/training_sessions.json')); q=d[0]['quiz'][0]; print(q)"

# -------------------------------
# Task 4: Implement Text-to-Speech System
# -------------------------------

nano src/tts_engine.py
ls -lh src/tts_engine.py

nano src/audio_manager.py
ls -lh src/audio_manager.py

nano test_tts.py
python test_tts.py

ls -lh audio/
cat data/audio_metadata.json

# -------------------------------
# Task 5: Build Complete Training System
# -------------------------------

nano main.py
nano demo.py

python demo.py

# -------------------------------
# Final Verification
# -------------------------------

ls -la data/
ls -la audio/
cat data/profiles.json
ls -la audio/*.mp3
ls -la audio/*.wav
