#!/usr/bin/env python3
"""
Content Validation Script
Completed validation checks (Ubuntu 24.04 compatible)
"""

import os
import subprocess
import json
from datetime import datetime


def _run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return (p.returncode == 0, p.stdout, p.stderr)
    except Exception as e:
        return (False, "", str(e))


def validate_video_file(video_path):
    """
    Validate video file integrity and properties.

    Returns:
        Dictionary with validation results
    """
    report = {
        "path": video_path,
        "exists": os.path.isfile(video_path),
        "readable": os.access(video_path, os.R_OK),
        "valid_ffprobe": False,
        "video_codec": None,
        "audio_codec": None,
        "duration_seconds": None,
        "resolution": None,
        "errors": []
    }

    if not report["exists"]:
        report["errors"].append("File does not exist")
        return report

    if not report["readable"]:
        report["errors"].append("File is not readable")
        return report

    cmd = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    ok, out, err = _run(cmd)
    if not ok:
        report["errors"].append(f"ffprobe failed: {err.strip()}")
        return report

    report["valid_ffprobe"] = True
    data = json.loads(out)

    # Duration extraction
    try:
        report["duration_seconds"] = round(float(data["format"]["duration"]), 2)
    except Exception:
        report["duration_seconds"] = None

    width = None
    height = None

    for s in data.get("streams", []):
        if s.get("codec_type") == "video" and report["video_codec"] is None:
            report["video_codec"] = s.get("codec_name")
            width = s.get("width")
            height = s.get("height")

        if s.get("codec_type") == "audio" and report["audio_codec"] is None:
            report["audio_codec"] = s.get("codec_name")

    if width and height:
        report["resolution"] = f"{width}x{height}"

    # Basic validation checks
    if report["video_codec"] is None:
        report["errors"].append("No video stream detected")

    if report["audio_codec"] is None:
        report["errors"].append("No audio stream detected (or audio missing)")

    if report["duration_seconds"] is not None and report["duration_seconds"] <= 0:
        report["errors"].append("Invalid duration")

    return report


def validate_distribution_package(base_dir=os.path.expanduser("~/security-training")):
    """
    Validate all distribution packages and processed content.
    """

    dist_dir = os.path.join(base_dir, "distribution")
    processed_dir = os.path.join(base_dir, "processed")

    channels = ["web", "mobile", "email"]

    results = {
        "validated_at": datetime.now().isoformat(),
        "base_dir": base_dir,
        "channels": {},
        "portal_exists": False,
        "processed_videos": [],
        "errors": []
    }

    # Validate processed videos
    if os.path.isdir(processed_dir):
        vids = [f for f in os.listdir(processed_dir) if f.lower().endswith(".mp4")]
        for v in vids:
            vp = os.path.join(processed_dir, v)
            results["processed_videos"].append(validate_video_file(vp))
    else:
        results["errors"].append("Processed directory missing")

    # Validate distribution channels
    for ch in channels:
        ch_dir = os.path.join(dist_dir, ch)

        if not os.path.isdir(ch_dir):
            results["channels"][ch] = {
                "exists": False,
                "count": 0,
                "files": []
            }
            results["errors"].append(f"Missing channel directory: {ch_dir}")
            continue

        files = [f for f in os.listdir(ch_dir) if f.lower().endswith(".mp4")]

        results["channels"][ch] = {
            "exists": True,
            "count": len(files),
            "files": []
        }

        for f in files:
            fp = os.path.join(ch_dir, f)
            vrep = validate_video_file(fp)

            size_mb = os.path.getsize(fp) / (1024 * 1024)
            vrep["size_mb"] = round(size_mb, 2)

            results["channels"][ch]["files"].append(vrep)

    # Validate web portal
    portal = os.path.join(dist_dir, "index.html")
    results["portal_exists"] = os.path.isfile(portal)

    if not results["portal_exists"]:
        results["errors"].append("Web portal index.html missing")

    # Sanity check: ensure at least one valid processed video exists
    processed_success = any(
        item.get("valid_ffprobe") for item in results["processed_videos"]
    )

    if processed_success:
        for ch in channels:
            if results["channels"].get(ch, {}).get("count", 0) == 0:
                results["errors"].append(f"No videos found in channel: {ch}")

    # Save validation report
    report_path = os.path.join(dist_dir, "validation_report.json")
    os.makedirs(dist_dir, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("[INFO] Validation completed.")
    print("[INFO] Report saved:", report_path)

    if results["errors"]:
        print("[WARN] Validation issues found:")
        for e in results["errors"]:
            print(" -", e)
    else:
        print("[INFO] No major validation issues detected.")

    return True


if __name__ == "__main__":
    validate_distribution_package()
