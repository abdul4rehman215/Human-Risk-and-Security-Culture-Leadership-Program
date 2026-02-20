from src.user_profile import UserProfileManager
from src.training_manager import TrainingManager


def test_content_generation():
    """Test personalized content generation."""
    profile_mgr = UserProfileManager()
    manager = TrainingManager()

    # Create test user profile
    user_id = "demo_user"
    profile_mgr.create_profile(
        user_id=user_id,
        name="Sara",
        experience_level="beginner",
        learning_style="visual",
        interests=["phishing", "password_security"],
    )

    # Generate lesson for specific topic
    lesson = manager.create_personalized_lesson(user_id, "phishing")

    # Print lesson content
    print("\n=== GENERATED LESSON CONTENT ===\n")
    print(lesson["content"])

    # Generate learning path
    path = manager.generate_learning_path(user_id)

    # Display results
    print("\n=== RECOMMENDED LEARNING PATH ===")
    for i, t in enumerate(path, start=1):
        print(f"{i}. {t}")


if __name__ == "__main__":
    test_content_generation()
