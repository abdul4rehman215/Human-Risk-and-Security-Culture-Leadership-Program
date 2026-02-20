# 🛠 Troubleshooting Guide - Lab 08: Building Training Content

> This section documents common issues encountered during the lab and their resolutions.  
> All fixes were tested in the Ubuntu 24.04 cloud lab environment.

# 🎥 OBS Studio Issues

---

## 1️⃣ Black Screen While Recording

### 🔎 Symptoms
- OBS preview window shows black screen
- Recording saved but contains blank video
- Screen capture source not visible

### 🧠 Cause
- Screen capture permissions not granted
- Wayland/X11 compatibility issue
- Incorrect capture source selected

### ✅ Resolution

1. Ensure correct source selected (Screen Capture XSHM on X11)
2. Restart OBS:

```bash
pkill obs
obs &
````

3. If running Wayland, switch to X11 session before login.

---

## 2️⃣ No Audio in Recording

### 🔎 Symptoms

* Video plays correctly
* No microphone or desktop audio captured

### 🧠 Cause

* PulseAudio misconfiguration
* Incorrect audio device selected in OBS

### ✅ Resolution

Restart PulseAudio:

```bash
pulseaudio --kill && pulseaudio --start
```

Verify OBS → Settings → Audio:

* Mic/Aux: Correct input device
* Desktop Audio: Default

---

## 3️⃣ Laggy or Stuttering Recording

### 🔎 Symptoms

* Video freezes
* Frame drops in recording

### 🧠 Cause

* High bitrate (5000 Kbps) on limited cloud resources
* CPU overload

### ✅ Resolution

Lower bitrate in OBS:

* Settings → Output
* Reduce bitrate to 3000 Kbps
* Change preset to "veryfast"

---

# 🎬 FFmpeg Processing Errors

---

## 4️⃣ Codec Not Found Error

### 🔎 Symptoms

* ffmpeg fails during encoding
* Error mentioning missing codec

### 🧠 Cause

* Missing multimedia codecs

### ✅ Resolution

Reinstall codecs:

```bash
sudo apt install --reinstall ubuntu-restricted-extras ffmpeg
```

Verify ffmpeg installation:

```bash
ffmpeg -version
```

---

## 5️⃣ Concat Operation Fails

### 🔎 Symptoms

* Intro/outro concatenation fails
* ffmpeg returns stream mismatch error

### 🧠 Cause

* Resolution mismatch
* Frame rate mismatch
* Pixel format mismatch

### ✅ Resolution

Ensure normalization step runs successfully:

```bash
ffmpeg -i input.mp4 -vf scale=1280:720,format=yuv420p -r 30 output.mp4
```

Verify resolution:

```bash
ffprobe -v error -show_streams input.mp4
```

---

## 6️⃣ Slow Video Processing

### 🔎 Symptoms

* ffmpeg encoding takes too long

### 🧠 Cause

* Default encoding preset is CPU-intensive

### ✅ Resolution

Use faster preset for testing:

```bash
-preset veryfast
```

In production, switch back to `fast` or `medium` for better compression.

---

# 📂 Distribution Issues

---

## 7️⃣ Missing Channel Directories

### 🔎 Symptoms

* Distribution script throws directory error
* Validation reports missing channel

### 🧠 Cause

* Script not executed from correct base directory
* Distribution folder manually deleted

### ✅ Resolution

Recreate directory structure:

```bash
mkdir -p ~/security-training/distribution/{web,mobile,email}
```

Re-run distribution:

```bash
python3 scripts/distribute_content.py
```

---

## 8️⃣ Web Portal Not Loading

### 🔎 Symptoms

* index.html does not open
* Blank browser page

### 🧠 Cause

* Missing distribution files
* Portal not generated

### ✅ Resolution

Regenerate portal:

```bash
python3 scripts/distribute_content.py
```

Open manually:

```bash
firefox ~/security-training/distribution/index.html &
```

---

# 🧪 Validation Errors

---

## 9️⃣ Validation Reports "No video stream detected"

### 🔎 Symptoms

* validation_report.json shows video stream error

### 🧠 Cause

* Corrupted MP4 file
* Improper encoding

### ✅ Resolution

Reprocess videos:

```bash
python3 scripts/video_processor.py
```

Revalidate:

```bash
python3 scripts/validate_content.py
```

---

## 🔟 Validation Reports Missing Channel Files

### 🔎 Symptoms

* One distribution channel empty
* Validation shows channel count = 0

### 🧠 Cause

* Distribution step skipped
* Script failed silently

### ✅ Resolution

Run full pipeline:

```bash
echo "Processing videos..."
python3 scripts/video_processor.py

echo "Distributing content..."
python3 scripts/distribute_content.py

echo "Validating content..."
python3 scripts/validate_content.py
```

---

# 🧹 Temporary File Cleanup

If processing fails or tmp files remain:

```bash
rm -rf /tmp/security_training_tmp
rm -rf /tmp/*.mp4
rm -rf /tmp/*.png
```

---

# 🧾 Best Practices Learned

* Always normalize resolution before concatenation
* Validate files using ffprobe before distribution
* Use CRF-based compression for predictable output size
* Separate production pipeline into:

  * Processing
  * Distribution
  * Validation

---

# ✅ Final Verification Checklist

✔ OBS recording saved in `videos/`
✔ Title and end cards generated
✔ Processed video created
✔ Multi-channel distribution available
✔ Web portal generated
✔ Validation report confirms integrity

---

✅ End of Troubleshooting – Lab 08
