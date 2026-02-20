#!/bin/bash
# Lab 08 - Building Training Content
# Commands Executed During Lab (sequential, clean)

# Task 1: Install and Configure OBS Studio
sudo apt update && sudo apt upgrade -y
sudo apt install -y obs-studio ffmpeg v4l2loopback-dkms
sudo apt install -y ubuntu-restricted-extras imagemagick

mkdir -p ~/security-training/{videos,graphics,scripts,processed,distribution}
cd ~/security-training

obs &

# Task 2: Creating Training Content
nano scripts/training-script.txt
nano graphics/phishing-example.html
firefox graphics/phishing-example.html &

ls -lh videos/

# Task 3: Creating Graphics and Visual Elements
convert -size 200x200 xc:transparent \
 -fill red -stroke black -strokewidth 3 \
 -draw "polygon 100,20 180,160 20,160" \
 -fill yellow -pointsize 72 -gravity center \
 -annotate +0+10 "!" \
 graphics/warning-icon.png

convert -size 200x200 xc:transparent \
 -fill blue -stroke darkblue -strokewidth 3 \
 -draw "path 'M 100,20 L 160,60 L 160,140 L 100,180 L 40,140 L 40,60 Z'" \
 graphics/shield-icon.png

ls -lh graphics/

convert -size 1920x1080 xc:'#1f4e79' \
 -fill white -font DejaVu-Sans-Bold -pointsize 72 \
 -gravity center -annotate +0-100 'PHISHING AWARENESS' \
 -fill yellow -pointsize 48 \
 -annotate +0+50 'Security Training Module' \
 graphics/title-card.png

convert -size 1920x1080 xc:'#2d5a2d' \
 -fill white -pointsize 64 \
 -gravity center -annotate +0-50 'Training Complete' \
 -fill lightgreen -pointsize 40 \
 -annotate +0+50 'Stay Vigilant!' \
 graphics/end-card.png

ls -lh graphics/

# Task 4: Automating Video Processing
nano scripts/video_processor.py
chmod +x scripts/video_processor.py

nano scripts/distribute_content.py
chmod +x scripts/distribute_content.py

python3 scripts/video_processor.py
ls -lh processed/

python3 scripts/distribute_content.py
ls -lh distribution/web/
ls -lh distribution/mobile/
ls -lh distribution/email/

# Task 5: Validation and Quality Assurance
nano scripts/validate_content.py
chmod +x scripts/validate_content.py

echo "Processing videos..."
python3 scripts/video_processor.py

echo "Distributing content..."
python3 scripts/distribute_content.py

echo "Validating content..."
python3 scripts/validate_content.py

tree ~/security-training

ls -lh ~/security-training/processed/

for channel in web mobile email; do
  echo "=== $channel channel ==="
  ls -lh ~/security-training/distribution/$channel/
done

firefox ~/security-training/distribution/index.html &
