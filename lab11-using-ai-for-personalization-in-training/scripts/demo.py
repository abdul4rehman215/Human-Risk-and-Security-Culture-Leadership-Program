from main import PersonalizedTrainingSystem


def run_demo():
    """Run interactive demonstration of the system."""
    system = PersonalizedTrainingSystem()

    print("=== Personalized Training System Demo ===\n")

    # Create sample users with different profiles
    users = [
        {
            "user_id": "user_beginner",
            "name": "Nida",
            "experience": "beginner",
            "learning_style": "visual",
            "interests": ["phishing", "password_security", "safe_browsing"],
        },
        {
            "user_id": "user_intermediate",
            "name": "Imran",
            "experience": "intermediate",
            "learning_style": "reading",
            "interests": ["incident_response", "social_engineering", "data_handling"],
        },
        {
            "user_id": "user_advanced",
            "name": "Faizan",
            "experience": "advanced",
            "learning_style": "auditory",
            "interests": ["cloud_security", "threat_hunting", "siem"],
        },
    ]

    onboarding_packages = {}
    for u in users:
        package = system.onboard_user(
            user_id=u["user_id"],
            name=u["name"],
            experience=u["experience"],
            learning_style=u["learning_style"],
            interests=u["interests"],
        )
        onboarding_packages[u["user_id"]] = package

    print("=== Onboarding Results ===")
    for uid, pkg in onboarding_packages.items():
        print(f"\nUser: {uid}")
        print("Profile:", pkg["profile"])
        print("Learning Path:", pkg["recommended_learning_path"])

    # Generate personalized lessons for each
    print("\n=== Deliver Lessons (Personalized) ===")
    lesson_bundles = []
    for u in users:
        # pick first interest as topic
        topic = u["interests"][0]
        bundle = system.deliver_lesson(u["user_id"], topic, include_audio=True)
        lesson_bundles.append(bundle)

        lesson = bundle["lesson"]
        print(f"\n--- Lesson for {u['name']} ({u['experience']} / {u['learning_style']}) ---")
        print(f"Topic: {lesson['topic']}")
        print("\nCONTENT PREVIEW (first 25 lines):")
        lines = lesson["content"].splitlines()
        preview = "\n".join(lines[:25])
        print(preview)

        if bundle["audio"]:
            print("\nAudio Sections:")
            for s in bundle["audio"]["sections"]:
                print(f"- {s['file_path']}")

        # Fake quiz score for demo
        quiz_score = 80 if u["experience"] != "advanced" else 90
        system.track_progress(u["user_id"], lesson["lesson_id"], quiz_score)

    # Display results and comparisons
    print("\n=== Progress Reports ===")
    for u in users:
        report = system.generate_report(u["user_id"])
        print(f"\nReport for {u['name']} ({u['user_id']}):")
        print(report)

    # Show how content adapts to different users
    print("\n=== Adaptation Demonstration ===")
    print("Notice how lesson intros, examples, and difficulty notes vary based on:")
    print("- experience_level (beginner/intermediate/advanced)")
    print("- learning_style (visual/auditory/reading/kinesthetic)")
    print("- interests (topics prioritized and referenced)")

    print("\nDemo completed!")


if __name__ == "__main__":
    run_demo()
