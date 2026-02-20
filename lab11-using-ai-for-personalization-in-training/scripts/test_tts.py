from src.user_profile import UserProfileManager
from src.training_manager import TrainingManager
from src.audio_manager import AudioManager


def test_tts_system():
    """Test text-to-speech functionality."""
    profile_mgr = UserProfileManager()
    training_mgr = TrainingManager()
    audio_mgr = AudioManager()

    # Create sample lesson
    user_id = "tts_user"
    profile_mgr.create_profile(
        user_id=user_id,
        name="Hina",
        experience_level="beginner",
        learning_style="auditory",
        interests=["phishing", "incident_reporting"],
    )

    lesson = training_mgr.create_personalized_lesson(user_id, "password_security")

    # Generate audio version
    metadata = audio_mgr.create_lesson_audio(
        lesson_id=lesson["lesson_id"],
        lesson_content=lesson["content"],
        preferences={"engine": "offline"},
    )

    # Verify audio file creation (by checking metadata paths)
    print("\n=== AUDIO METADATA ===")
    print(metadata)

    print("\n=== GENERATED AUDIO FILES ===")
    for s in metadata["sections"]:
        print(f"- {s['file_path']} (est. {s['estimated_duration_seconds']}s)")


if __name__ == "__main__":
    test_tts_system()
