from src.user_profile import UserProfileManager


def test_profile_system():
    """Test the profile management system."""
    manager = UserProfileManager()

    # Create test profiles for different user types
    p1 = manager.create_profile(
        user_id="u001",
        name="Ayesha",
        experience_level="beginner",
        learning_style="visual",
        interests=["phishing", "password_security", "safe_browsing"],
    )

    p2 = manager.create_profile(
        user_id="u002",
        name="Rohan",
        experience_level="intermediate",
        learning_style="reading",
        interests=["network_security", "incident_response", "malware"],
    )

    p3 = manager.create_profile(
        user_id="u003",
        name="Zain",
        experience_level="advanced",
        learning_style="auditory",
        interests=["threat_hunting", "siem", "cloud_security"],
    )

    print("=== Created Profiles ===")
    print(p1)
    print(p2)
    print(p3)

    # Test profile retrieval
    print("\n=== Retrieve Profile u002 ===")
    retrieved = manager.get_profile("u002")
    print(retrieved)

    # Test profile updates
    print("\n=== Update Profile u001 (add completed module + quiz history) ===")
    updated = manager.update_profile(
        "u001",
        {
            "completed_modules": ["phishing_basics"],
            "quiz_history": [{"lesson_id": "phishing_basics", "score": 80, "timestamp": "demo"}],
        },
    )
    print(updated)

    print("\n=== Final Profiles File Content (loaded) ===")
    all_profiles = manager.load_profiles()
    print(all_profiles)


if __name__ == "__main__":
    test_profile_system()
