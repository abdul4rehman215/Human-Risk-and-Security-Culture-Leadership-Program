#!/usr/bin/env python3
"""
Video Processing Automation
Complete implementation (Ubuntu 24.04 compatible)
"""

import os
import subprocess
import json
from datetime import datetime


class VideoProcessor:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.videos_dir = os.path.join(base_dir, "videos")
        self.graphics_dir = os.path.join(base_dir, "graphics")
        self.processed_dir = os.path.join(base_dir, "processed")
        os.makedirs(self.processed_dir, exist_ok=True)

    def _run(self, cmd):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return (p.returncode == 0, p.stdout, p.stderr)
        except Exception as e:
            return (False, "", str(e))

    def get_video_info(self, video_path):
        cmd = [
            "ffprobe", "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        ok, out, err = self._run(cmd)
        if not ok:
            return {"error": err.strip(), "path": video_path}

        data = json.loads(out)
        duration = 0.0
        if "format" in data and "duration" in data["format"]:
            try:
                duration = float(data["format"]["duration"])
            except Exception:
                duration = 0.0

        vcodec = None
        acodec = None
        width = None
        height = None

        for s in data.get("streams", []):
            if s.get("codec_type") == "video" and vcodec is None:
                vcodec = s.get("codec_name")
                width = s.get("width")
                height = s.get("height")
            if s.get("codec_type") == "audio" and acodec is None:
                acodec = s.get("codec_name")

        return {
            "path": video_path,
            "duration_seconds": round(duration, 2),
            "video_codec": vcodec,
            "audio_codec": acodec,
            "resolution": f"{width}x{height}" if width and height else None,
        }

    def add_intro_outro(self, input_video, output_video, title_card, end_card):
        try:
            tmp_dir = "/tmp/security_training_tmp"
            os.makedirs(tmp_dir, exist_ok=True)

            intro = os.path.join(tmp_dir, "intro.mp4")
            outro = os.path.join(tmp_dir, "outro.mp4")

            cmd_intro = [
                "ffmpeg", "-y",
                "-loop", "1", "-t", "3",
                "-i", title_card,
                "-vf", "scale=1280:720,format=yuv420p",
                "-r", "30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                intro
            ]
            ok, _, err = self._run(cmd_intro)
            if not ok:
                print("[ERROR] Intro creation failed:", err.strip())
                return False

            cmd_outro = [
                "ffmpeg", "-y",
                "-loop", "1", "-t", "3",
                "-i", end_card,
                "-vf", "scale=1280:720,format=yuv420p",
                "-r", "30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                outro
            ]
            ok, _, err = self._run(cmd_outro)
            if not ok:
                print("[ERROR] Outro creation failed:", err.strip())
                return False

            normalized_main = os.path.join(tmp_dir, "main_norm.mp4")
            cmd_norm = [
                "ffmpeg", "-y",
                "-i", input_video,
                "-vf", "scale=1280:720,format=yuv420p",
                "-r", "30",
                "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k",
                normalized_main
            ]
            ok, _, err = self._run(cmd_norm)
            if not ok:
                print("[ERROR] Main normalization failed:", err.strip())
                return False

            concat_list = os.path.join(tmp_dir, "concat_list.txt")
            with open(concat_list, "w", encoding="utf-8") as f:
                f.write(f"file '{intro}'\n")
                f.write(f"file '{normalized_main}'\n")
                f.write(f"file '{outro}'\n")

            cmd_concat = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_list,
                "-c", "copy",
                output_video
            ]
            ok, _, err = self._run(cmd_concat)
            if not ok:
                cmd_concat_re = [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0",
                    "-i", concat_list,
                    "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k",
                    output_video
                ]
                ok2, _, err2 = self._run(cmd_concat_re)
                if not ok2:
                    print("[ERROR] Concat failed:", err.strip(), err2.strip())
                    return False

            return True
        except Exception as e:
            print("[ERROR] add_intro_outro exception:", str(e))
            return False

    def compress_video(self, input_video, output_video, quality="medium"):
        crf_map = {
            "high": "20",
            "medium": "23",
            "low": "28"
        }
        crf = crf_map.get(quality, "23")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", crf,
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            output_video
        ]
        ok, _, err = self._run(cmd)
        if not ok:
            print("[ERROR] Compression failed:", err.strip())
            return False
        return True

    def process_all_videos(self):
        if not os.path.isdir(self.videos_dir):
            print("[ERROR] videos directory not found:", self.videos_dir)
            return False

        title_card = os.path.join(self.graphics_dir, "title-card.png")
        end_card = os.path.join(self.graphics_dir, "end-card.png")

        if not os.path.isfile(title_card) or not os.path.isfile(end_card):
            print("[ERROR] Missing title/end cards.")
            return False

        videos = [f for f in os.listdir(self.videos_dir) if f.lower().endswith((".mp4", ".mkv", ".mov", ".avi"))]
        if not videos:
            print("[WARN] No videos found.")
            return False

        report = {
            "processed_at": datetime.now().isoformat(),
            "items": []
        }

        for v in videos:
            in_path = os.path.join(self.videos_dir, v)
            base_name, _ = os.path.splitext(v)

            with_intro = os.path.join(self.processed_dir, f"{base_name}_intro_outro.mp4")
            compressed = os.path.join(self.processed_dir, f"{base_name}_compressed.mp4")

            print(f"[INFO] Processing: {v}")

            ok_intro = self.add_intro_outro(in_path, with_intro, title_card, end_card)
            if not ok_intro:
                report["items"].append({"input": in_path, "status": "failed_intro_outro"})
                continue

            ok_comp = self.compress_video(with_intro, compressed, quality="medium")
            if not ok_comp:
                report["items"].append({"input": in_path, "status": "failed_compress"})
                continue

            meta = self.get_video_info(compressed)

            report["items"].append({
                "input": in_path,
                "compressed": compressed,
                "metadata": meta,
                "status": "success"
            })

        report_path = os.path.join(self.processed_dir, "processing_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print("[INFO] Processing complete.")
        print("[INFO] Report saved:", report_path)
        return True


if __name__ == "__main__":
    processor = VideoProcessor(os.path.expanduser("~/security-training"))
    processor.process_all_videos()
