import os
import re
import pyttsx3
from gtts import gTTS


class TTSEngine:
    def __init__(self, output_dir="audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Initialize pyttsx3 engine
        self.engine = pyttsx3.init()

        # Configure voice properties (rate, volume)
        # These are safe defaults; users can override via AudioManager preferences later.
        self.engine.setProperty("rate", 170)   # speaking rate
        self.engine.setProperty("volume", 1.0) # volume 0.0 - 1.0

    def text_to_speech_offline(self, text, filename):
        """
        Convert text to speech using offline engine (pyttsx3).

        Returns:
            Path to generated audio file
        """
        clean = self.clean_text_for_tts(text)

        # NOTE: pyttsx3 output format depends on system drivers.
        # On many Linux systems, saving directly to mp3 is not supported.
        # We use WAV for offline output to be reliable.
        out_path = os.path.join(self.output_dir, f"{filename}.wav")

        # Generate audio file
        self.engine.save_to_file(clean, out_path)
        self.engine.runAndWait()

        return out_path

    def text_to_speech_online(self, text, filename, lang="en"):
        """
        Convert text to speech using Google TTS (requires internet).

        Returns:
            Path to generated audio file
        """
        clean = self.clean_text_for_tts(text)
        out_path = os.path.join(self.output_dir, f"{filename}.mp3")

        tts = gTTS(text=clean, lang=lang)
        tts.save(out_path)

        return out_path

    def clean_text_for_tts(self, text):
        """
        Remove markdown formatting and clean text for TTS.
        """
        if not text:
            return ""

        cleaned = text

        # Remove code blocks ```...```
        cleaned = re.sub(r"```.*?```", " ", cleaned, flags=re.DOTALL)

        # Remove markdown headers (# ## ###)
        cleaned = re.sub(r"^\s*#{1,6}\s*", "", cleaned, flags=re.MULTILINE)

        # Remove bold/italic markers (* ** _ __)
        cleaned = cleaned.replace("**", "")
        cleaned = cleaned.replace("*", "")
        cleaned = cleaned.replace("__", "")
        cleaned = cleaned.replace("_", "")

        # Remove inline code markers `
        cleaned = cleaned.replace("`", "")

        # Remove bullet points and numbering at line start
        cleaned = re.sub(r"^\s*[-•]\s+", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.MULTILINE)

        # Replace multiple newlines with single newline
        cleaned = re.sub(r"\n{2,}", "\n", cleaned)

        # Clean extra whitespace
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        cleaned = cleaned.strip()

        return cleaned

    def create_lesson_audio(self, lesson_content, lesson_id, engine="offline"):
        """
        Create audio version of entire lesson.
        """
        clean = self.clean_text_for_tts(lesson_content)
        safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(lesson_id))

        if engine == "online":
            return self.text_to_speech_online(clean, safe_id)
        else:
            return self.text_to_speech_offline(clean, safe_id)
