#!/usr/bin/env python3
"""
Content Distribution Manager
Complete distribution logic (Ubuntu 24.04 compatible)
"""

import os
import subprocess
import shutil
from datetime import datetime
import json


class ContentDistributor:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.processed_dir = os.path.join(base_dir, "processed")
        self.distribution_dir = os.path.join(base_dir, "distribution")

        # Create distribution channels
        self.channels = {
            "web": os.path.join(self.distribution_dir, "web"),
            "mobile": os.path.join(self.distribution_dir, "mobile"),
            "email": os.path.join(self.distribution_dir, "email"),
        }

        os.makedirs(self.distribution_dir, exist_ok=True)
        for channel_dir in self.channels.values():
            os.makedirs(channel_dir, exist_ok=True)

    def _run(self, cmd):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return (p.returncode == 0, p.stdout, p.stderr)
        except Exception as e:
            return (False, "", str(e))

    def create_web_version(self, video_file):
        """
        Create web-optimized video (720p, streaming-ready).
        CRF 23 + faststart
        """
        src = os.path.join(self.processed_dir, video_file)
        dst = os.path.join(self.channels["web"], video_file.replace(".mp4", "_web_720p.mp4"))

        cmd = [
            "ffmpeg", "-y",
            "-i", src,
            "-vf", "scale=1280:720",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            dst
        ]
        ok, _, err = self._run(cmd)
        if not ok:
            print("[ERROR] Web version failed:", err.strip())
            return None
        return dst

    def create_mobile_version(self, video_file):
        """
        Create mobile-optimized video (360p, smaller file).
        Baseline profile for compatibility
        """
        src = os.path.join(self.processed_dir, video_file)
        dst = os.path.join(self.channels["mobile"], video_file.replace(".mp4", "_mobile_360p.mp4"))

        cmd = [
            "ffmpeg", "-y",
            "-i", src,
            "-vf", "scale=640:360",
            "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
            "-crf", "28", "-preset", "fast",
            "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart",
            dst
        ]
        ok, _, err = self._run(cmd)
        if not ok:
            print("[ERROR] Mobile version failed:", err.strip())
            return None
        return dst

    def create_email_version(self, video_file):
        """
        Create email-friendly video (480p, compressed).
        CRF 28
        """
        src = os.path.join(self.processed_dir, video_file)
        dst = os.path.join(self.channels["email"], video_file.replace(".mp4", "_email_480p.mp4"))

        cmd = [
            "ffmpeg", "-y",
            "-i", src,
            "-vf", "scale=854:480",
            "-c:v", "libx264", "-crf", "28", "-preset", "fast",
            "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart",
            dst
        ]
        ok, _, err = self._run(cmd)
        if not ok:
            print("[ERROR] Email version failed:", err.strip())
            return None
        return dst

    def generate_web_portal(self):
        """
        Generate HTML page for video distribution.
        Saves: distribution/index.html
        """
        web_files = sorted([
            f for f in os.listdir(self.channels["web"])
            if f.lower().endswith(".mp4")
        ])

        html_path = os.path.join(self.distribution_dir, "index.html")
        lines = []
        lines.append("<!DOCTYPE html>")
        lines.append("<html><head><meta charset='utf-8'>")
        lines.append("<title>Security Training Portal</title>")
        lines.append("<style>")
        lines.append("body{font-family:Arial;margin:20px;max-width:1000px}")
        lines.append(".card{border:1px solid #ddd;padding:15px;margin:15px 0;border-radius:8px}")
        lines.append("video{width:100%;max-width:900px}")
        lines.append("</style></head><body>")
        lines.append("<h1>Security Training Portal</h1>")
        lines.append("<p>Download versions: Web (720p), Mobile (360p), Email (480p)</p>")

        for wf in web_files:
            base = wf.replace("_web_720p.mp4", "")
            mobile = f"{base}_mobile_360p.mp4"
            email = f"{base}_email_480p.mp4"

            lines.append("<div class='card'>")
            lines.append(f"<h2>{base}</h2>")
            lines.append(f"<video controls src='web/{wf}'></video><br><br>")
            lines.append("<strong>Downloads:</strong><br>")
            lines.append(f"<a href='web/{wf}' download>Web 720p</a><br>")

            if os.path.exists(os.path.join(self.channels["mobile"], mobile)):
                lines.append(f"<a href='mobile/{mobile}' download>Mobile 360p</a><br>")

            if os.path.exists(os.path.join(self.channels["email"], email)):
                lines.append(f"<a href='email/{email}' download>Email 480p</a><br>")

            lines.append("</div>")

        lines.append("</body></html>")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return html_path

    def distribute_all(self):
        """Distribute all processed videos to channels."""
        if not os.path.isdir(self.processed_dir):
            print("[ERROR] processed directory not found:", self.processed_dir)
            return False

        processed_videos = [
            f for f in os.listdir(self.processed_dir)
            if f.lower().endswith(".mp4")
        ]

        if not processed_videos:
            print("[WARN] No processed videos found in:", self.processed_dir)
            return False

        report = {
            "distributed_at": datetime.now().isoformat(),
            "processed_dir": self.processed_dir,
            "distribution_dir": self.distribution_dir,
            "items": []
        }

        for v in processed_videos:
            print("[INFO] Distributing:", v)

            web_path = self.create_web_version(v)
            mob_path = self.create_mobile_version(v)
            eml_path = self.create_email_version(v)

            report["items"].append({
                "source": os.path.join(self.processed_dir, v),
                "web": web_path,
                "mobile": mob_path,
                "email": eml_path,
            })

        portal = self.generate_web_portal()
        report["web_portal"] = portal

        report_path = os.path.join(self.distribution_dir, "distribution_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print("[INFO] Distribution complete.")
        print("[INFO] Portal:", portal)
        print("[INFO] Report:", report_path)
        return True


if __name__ == "__main__":
    distributor = ContentDistributor(os.path.expanduser("~/security-training"))
    distributor.distribute_all()
