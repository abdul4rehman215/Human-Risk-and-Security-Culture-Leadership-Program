import json
import os
from datetime import datetime

from src.tts_engine import TTSEngine


class AudioManager:
    def __init__(self):
        self.tts_engine = TTSEngine()
        self.metadata_file = "data/audio_metadata.json"
        os.makedirs("data", exist_ok=True)

    def create_lesson_audio(self, lesson_id, lesson_content, preferences=None):
        """
        Create audio version with metadata tracking.

        Returns:
            Audio metadata dictionary
        """
        preferences = preferences or {}

        engine = preferences.get("engine", "offline")  # offline or online
        lang = preferences.get("lang", "en")

        # Split content into sections if needed
        sections = self.split_content_into_sections(lesson_content)

        audio_files = []
        total_estimated_seconds = 0

        # Generate audio for each section
        for idx, section in enumerate(sections, start=1):
            section_title = section.get("title", f"section_{idx}")
            section_text = section.get("content", "")

            filename = f"{lesson_id}_{idx:02d}_{section_title}".replace(" ", "_")

            if engine == "online":
                path = self.tts_engine.text_to_speech_online(section_text, filename, lang=lang)
            else:
                path = self.tts_engine.text_to_speech_offline(section_text, filename)

            duration = self.estimate_duration(section_text)
            total_estimated_seconds += duration

            audio_files.append(
                {
                    "section_index": idx,
                    "title": section.get("title"),
                    "file_path": path,
                    "estimated_duration_seconds": duration,
                }
            )

        # Create metadata object
        metadata = {
            "lesson_id": str(lesson_id),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "engine": engine,
            "lang": lang,
            "sections": audio_files,
            "estimated_total_duration_seconds": total_estimated_seconds,
        }

        # Save metadata
        all_meta = self._load_metadata()
        all_meta[str(lesson_id)] = metadata
        self._save_metadata(all_meta)

        return metadata

    def split_content_into_sections(self, content):
        """
        Split long content into manageable audio sections.

        Strategy:
        - Split by markdown headers (#, ##, ###)
        - If no headers, return a single section
        """
        if not content:
            return [{"title": "lesson", "content": ""}]

        lines = content.splitlines()
        sections = []
        current_title = "lesson"
        current_lines = []

        header_pattern = r"^\s*#{1,6}\s+(.+)$"

        for line in lines:
            m = __import__("re").match(header_pattern, line)
            if m:
                # save previous
                if current_lines:
                    sections.append({"title": current_title.strip(), "content": "\n".join(current_lines).strip()})
                    current_lines = []
                current_title = m.group(1)
            else:
                current_lines.append(line)

        # last section
        if current_lines:
            sections.append({"title": current_title.strip(), "content": "\n".join(current_lines).strip()})

        # If splitting created too many tiny sections, merge very small ones
        merged = []
        buffer = None
        for s in sections:
            if buffer is None:
                buffer = s
            else:
                # If buffer content is too short, merge into it
                if len(buffer["content"]) < 400:
                    buffer["content"] = (buffer["content"] + "\n" + s["content"]).strip()
                else:
                    merged.append(buffer)
                    buffer = s
        if buffer:
            merged.append(buffer)

        return merged if merged else [{"title": "lesson", "content": content}]

    def get_audio_metadata(self, lesson_id):
        """Retrieve audio metadata for a lesson."""
        all_meta = self._load_metadata()
        return all_meta.get(str(lesson_id))

    def estimate_duration(self, text):
        """
        Estimate audio duration based on text length.
        Average speaking rate ~150 words/minute.
        """
        if not text:
            return 0
        words = len(text.split())
        words_per_minute = 150
        minutes = words / words_per_minute
        seconds = int(minutes * 60)
        return max(1, seconds)

    def _load_metadata(self):
        if not os.path.exists(self.metadata_file):
            return {}
        try:
            with open(self.metadata_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except json.JSONDecodeError:
            return {}
        except Exception:
            return {}

    def _save_metadata(self, meta):
        with open(self.metadata_file, "w") as f:
            json.dump(meta, f, indent=2)
