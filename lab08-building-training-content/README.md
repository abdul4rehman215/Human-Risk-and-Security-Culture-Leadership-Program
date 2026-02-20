# 🧪 Lab 08: Building Training Content

## 🎯 Objectives

By the end of this lab, I was able to:

- Install and configure **OBS Studio** for recording security awareness videos
- Create professional training content using screen recording techniques
- Design graphics and visual elements for training materials (ImageMagick)
- Develop Python scripts to automate **ffmpeg** processing workflows
- Implement a complete content creation + distribution + validation pipeline

---

## 📌 Prerequisites

- Basic Linux command line proficiency
- Fundamental Python programming knowledge
- Understanding of file system operations
- Familiarity with video formats (MP4, AVI)
- Basic security awareness concepts

---

Environment: **Ubuntu 24.04.1 LTS (Cloud Lab Environment)**  
User: **toor**  
Interface: **ens5**

---

## 🧱 Repository Structure

```text
lab08-building-training-content/
├── README.md
├── commands.sh
├── output.txt
├── interview_qna.md
├── troubleshooting.md
├── videos/
│   └── phishing-awareness-recording.mp4
├── graphics/
│   ├── phishing-example.html
│   ├── warning-icon.png
│   ├── shield-icon.png
│   ├── title-card.png
│   └── end-card.png
├── scripts/
│   ├── training-script.txt
│   ├── video_processor.py
│   ├── distribute_content.py
│   └── validate_content.py
├── processed/
│   ├── phishing-awareness-recording_intro_outro.mp4
│   ├── phishing-awareness-recording_compressed.mp4
│   └── processing_report.json
└── distribution/
    ├── web/
    │   └── phishing-awareness-recording_web_720p.mp4
    ├── mobile/
    │   └── phishing-awareness-recording_mobile_360p.mp4
    ├── email/
    │   └── phishing-awareness-recording_email_480p.mp4
    ├── index.html
    ├── distribution_report.json
    └── validation_report.json
```

---

## 🧩 Task 1: Installing and Configuring OBS Studio

### ✅ Step 1: Install Required Software

* Installed OBS Studio + ffmpeg + v4l2loopback
* Verified multimedia tools and codecs availability

### ✅ Step 2: Configure OBS Studio (Manual)

**OBS Settings Applied**

* Auto Wizard: Skipped
* Output Mode: Advanced
* Recording Path: `/home/toor/security-training/videos`
* Format: MP4
* Encoder: x264
* Bitrate: 5000 Kbps

### ✅ Step 3: Create Recording Scenes

Scenes created successfully:

* Desktop Demo
* Presenter Mode

Webcam resized bottom-right (**300x200**)

---

## 🧩 Task 2: Creating Training Content

### ✅ Step 1: Prepare Training Script

Created a structured narration script:

* Introduction
* Phishing definition
* Warning signs (5 core indicators)
* Real examples section
* Conclusion + reporting guidance

### ✅ Step 2: Create Sample Phishing Email (HTML)

Built a realistic phishing-style email page for on-screen recording:

* Urgent red header
* Suspicious sender address
* Threat-based language
* “Verify Now” link prompt

### ✅ Step 3: Record Training Video

OBS recording performed:

* Opened `phishing-example.html`
* Explained warning signs while demonstrating
* Recorded ~3 minutes
* Confirmed MP4 file saved in `videos/`

---

## 🧩 Task 3: Creating Graphics and Visual Elements

### ✅ Step 1: Generate Warning Icons (ImageMagick)

Generated:

* `warning-icon.png` (triangle + exclamation)
* `shield-icon.png` (security shield)

### ✅ Step 2: Create Title & End Cards (1080p)

Generated:

* `title-card.png` (PHISHING AWARENESS + module label)
* `end-card.png` (Training Complete + Stay Vigilant)

These assets are later injected into video processing automation.

---

## 🧩 Task 4: Automating Video Processing

### ✅ Video Processing Automation (Python + ffmpeg)

Created `scripts/video_processor.py` to:

* Extract metadata using **ffprobe**
* Generate intro/outro from PNG cards (3 seconds each)
* Normalize resolution to 1280x720 for safe concat
* Concatenate intro + main + outro
* Compress final output for distribution
* Generate `processed/processing_report.json`

---

## 🧩 Task 5: Distribution + Validation Pipeline

### ✅ Distribution Automation

Created `scripts/distribute_content.py` to:

* Create channel-specific outputs:

  * Web (720p)
  * Mobile (360p)
  * Email (480p)
* Generate `distribution/index.html` as a training portal
* Produce `distribution_report.json`

### ✅ Validation Automation

Created `scripts/validate_content.py` to:

* Verify file exists + readable
* Validate with ffprobe
* Check codec, duration, resolution
* Validate distribution directories and ensure portal exists
* Generate `validation_report.json`

---

## ✅ Result

* OBS recording completed and stored in `videos/`
* Title/end graphics created successfully using ImageMagick
* Automated processing pipeline produced:

  * Intro/outro version
  * Compressed distribution master
  * JSON processing report
* Multi-channel distribution generated (web/mobile/email)
* Validation completed with **no major issues**

---

## 🧠 What I Learned

* How to build real training content workflows (record → produce → distribute → validate)
* How to use **ImageMagick** for fast training graphics creation
* How to automate video production using **ffmpeg + Python**
* How to build structured reporting using JSON (processing, distribution, validation)

---

## 🌍 Why This Matters

Security culture is not only policies — it’s communication.
A repeatable training pipeline enables:

* Faster content creation
* Consistent messaging
* Scalable distribution across teams
* Quality control through automation

---

## 🚀 Real-World Applications

Used directly in:

* Enterprise phishing awareness programs
* HR / compliance training delivery
* SOC culture enablement and onboarding
* Internal security communications / campaigns
* Training portals and LMS content preparation

---

## ✅ Conclusion

This lab demonstrated a complete professional security training production pipeline:

* OBS-based recording
* Graphic asset creation
* Automated ffmpeg processing
* Multi-channel distribution (web/mobile/email)
* Validation & QA automation

This workflow reflects real-world security awareness content production used in organizations.

✅ **END OF LAB 08**
