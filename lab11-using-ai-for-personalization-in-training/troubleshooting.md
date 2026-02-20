# 🛠 Troubleshooting Guide – Lab 11: Using AI for Personalization in Training (Ubuntu 24.04)

> This guide covers common issues you may encounter while running the lab and practical solutions to resolve them.

---

# 1️⃣ Virtual Environment Issues

## ❌ Problem: `venv` not activating
Error:
`source: not found`
or prompt does not change to (`venv`)

### ✅ Solution:
Make sure you are using bash:
bash
```source venv/bin/activate```

If still not working:
sudo apt install python3-venv
```python3 -m venv venv```

---

## ❌ Problem: Wrong Python version
Check version:
```python --version```

If not Python 3.12+:
```
sudo apt update
sudo apt install python3
```
---

# 2️⃣ Package Installation Problems

## ❌ Problem: pip install fails
Common causes:
- No internet access
- DNS issues
- Firewall restrictions

### ✅ Solution:
Check connectivity:
```ping google.com```

Upgrade pip:
```pip install --upgrade pip```

Reinstall packages:
```pip install openai python-dotenv flask pyttsx3 gtts```

---

## ❌ Problem: ModuleNotFoundError
Example:
1ModuleNotFoundError: No module named `dotenv`

### ✅ Solution:
Ensure you are inside virtual environment:
```
which python
which pip
```

Reinstall missing package:
```
pip install python-dotenv
```
---

# 3️⃣ .env / API Issues

## ❌ Problem: demo_mode is False unexpectedly

### ✅ Solution:
Check .env file:
```
cat .env
```

Ensure:
```OPENAI_API_KEY=demo_key```

Restart terminal session after editing .env.

---

## ❌ Problem: Real API call fails

Error:
`[ERROR calling AI API]`

### ✅ Solution:
- Verify API key is valid
- Ensure internet access
- Check model name
- Confirm correct OpenAI package version

For lab purposes, use:
```OPENAI_API_KEY=demo_key```

---

# 4️⃣ Profile Not Saving

## ❌ Problem: data/profiles.json not created

### ✅ Solution:
Check directory permissions:
```ls -ld data/```

Fix permissions:
```chmod 755 data/```

Ensure disk space:
```
df -h
```
---

## ❌ Problem: JSON corrupted

Error:
`json.decoder.JSONDecodeError`

### ✅ Solution:
Delete corrupted file:
```
rm data/profiles.json
```
Re-run:
```
python test_profiles.py
```
---

# 5️⃣ Content Generation Problems

## ❌ Problem: Empty lesson content

### ✅ Solution:
Check:
- user profile exists
- topic string is valid
- demo_mode enabled

Test manually:
python -c "from src.content_generator import AIContentGenerator; print(AIContentGenerator().generate_personalized_content({'name':'Test','experience_level':'beginner','learning_style':'visual','interests':['phishing']}, 'phishing'))"

---

# 6️⃣ TTS Engine Problems (Most Common on Ubuntu)

## ❌ Problem: pyttsx3 fails silently

### ✅ Solution:
Upgrade:
```
pip install --upgrade pyttsx3
```

Install required audio libs:
sudo apt install espeak
sudo apt install libespeak1

Restart system if needed.

---

## ❌ Problem: No .wav file created

### ✅ Solution:
Check audio directory:
```
ls -la audio/
```
Ensure no permission issues:
```
chmod 755 audio/
```
Test simple TTS:
```
python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"
```
---

## ❌ Problem: Want MP3 but only WAV generated

### Explanation:
Offline engine (pyttsx3) on Linux reliably exports WAV only.

### ✅ Solution:
Use online engine:

preferences={"engine": "online"}
Note: Requires internet.

---

# 7️⃣ Audio Metadata Issues

## ❌ Problem: audio_metadata.json empty

### ✅ Solution:
Ensure lesson audio was created:
```
python test_tts.py
```
Check:
```
cat data/audio_metadata.json
```
If corrupted:
```
rm data/audio_metadata.json
Re-run test.
```

---

# 8️⃣ Demo Script Errors

## ❌ Problem: ValueError: User profile not found

### Cause:
deliver_lesson() called before onboarding.

### ✅ Solution:
Ensure onboarding runs first:

`
system.onboard_user(...)
`

---

## ❌ Problem: Duplicate lesson IDs

### Explanation:
Timestamp-based ID prevents collision.
If collision occurs, system clock may be incorrect.

### ✅ Solution:
Check system time:
```date```

---

# 9️⃣ File Permission Errors

## ❌ Problem: Permission denied

### ✅ Solution:
Check ownership:
```ls -la```

Fix:
```
sudo chown -R toor:toor ai-training-lab/
chmod -R 755 ai-training-lab/
```
---

# 🔟 General Debugging Tips

✔ Run scripts individually (test_profiles.py, test_content.py, test_tts.py)  
✔ Add temporary print() statements  
✔ Verify JSON files manually  
✔ Confirm virtual environment is active  
✔ Check for typos in topic names  
✔ Validate Python imports  

---

# 🧠 Advanced Troubleshooting (For Interviews)

If something fails in production:

1. Enable structured logging
2. Add try/except blocks with logging
3. Implement health checks
4. Add API rate limit handling
5. Use database instead of JSON files
6. Monitor disk space and memory

---

# ✅ Final Verification Checklist

- profiles.json exists
- training_sessions.json exists
- audio_metadata.json exists
- .wav files generated
- demo.py runs without error
- demo_mode=True in lab

---

# 🎯 Summary

Most lab issues fall into one of these categories:
- Virtual environment not activated
- Missing Python packages
- File permission errors
- Audio dependencies missing
- Incorrect .env configuration

Following this guide should resolve 95% of common Ubuntu 24.04 lab issues.
