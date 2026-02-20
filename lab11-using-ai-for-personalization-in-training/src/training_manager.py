import json
import os
from datetime import datetime

from src.user_profile import UserProfileManager
from src.content_generator import AIContentGenerator


class TrainingManager:
    def __init__(self):
        self.profile_manager = UserProfileManager()
        self.content_generator = AIContentGenerator()
        self.sessions_file = "data/training_sessions.json"
        os.makedirs("data", exist_ok=True)

    def create_personalized_lesson(self, user_id, topic):
        """
        Create complete personalized lesson for user.
        """
        # Get user profile
        profile = self.profile_manager.get_profile(user_id)
        if not profile:
            raise ValueError(f"User profile not found for user_id={user_id}")

        # Generate personalized content
        content = self.content_generator.generate_personalized_content(profile, topic)

        # Generate quiz questions
        quiz = self.content_generator.generate_quiz(profile, topic, num_questions=5)

        # Create lesson structure with metadata
        lesson_id = f"{user_id}_{topic}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        lesson = {
            "lesson_id": lesson_id,
            "user_id": str(user_id),
            "topic": topic,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "experience_level": profile.get("experience_level"),
            "learning_style": profile.get("learning_style"),
            "interests": profile.get("interests", []),
            "content": content,
            "quiz": quiz,
        }

        # Save lesson to file
        self.save_lesson(lesson)

        return lesson

    def generate_learning_path(self, user_id):
        """
        Generate personalized learning path based on user profile.
        """
        profile = self.profile_manager.get_profile(user_id)
        if not profile:
            raise ValueError(f"User profile not found for user_id={user_id}")

        exp = profile.get("experience_level", "beginner")
        interests = profile.get("interests", [])

        # Define topic sequences for each experience level
        beginner_path = [
            "phishing",
            "password_security",
            "safe_browsing",
            "device_security",
            "incident_reporting",
        ]

        intermediate_path = [
            "phishing",
            "password_security",
            "mfa_and_authentication",
            "data_handling",
            "incident_response",
            "social_engineering",
        ]

        advanced_path = [
            "threat_modeling",
            "incident_response",
            "cloud_security",
            "siem_basics",
            "threat_hunting",
            "security_controls",
        ]

        if exp == "beginner":
            base = beginner_path
        elif exp == "intermediate":
            base = intermediate_path
        else:
            base = advanced_path

        # Prioritize based on user interests
        # Put interests first (in same order), then remaining base topics
        ordered = []
        for t in interests:
            if t not in ordered:
                ordered.append(t)

        for t in base:
            if t not in ordered:
                ordered.append(t)

        return ordered

    def save_lesson(self, lesson):
        """Save lesson to persistent storage."""
        sessions = self._load_sessions()
        sessions.append(lesson)
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)

    def _load_sessions(self):
        if not os.path.exists(self.sessions_file):
            return []
        try:
            with open(self.sessions_file, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []
        except Exception:
            return []

    def get_user_progress(self, user_id):
        """Get user's training progress and statistics."""
        sessions = self._load_sessions()
        user_sessions = [s for s in sessions if str(s.get("user_id")) == str(user_id)]

        completed = len(user_sessions)
        topics = sorted(list({s.get("topic") for s in user_sessions if s.get("topic")}))

        avg_quiz_score = None
        quiz_scores = []
        for s in user_sessions:
            # quiz score not stored automatically; this will be tracked in main system
            # but we still calculate if it exists
            if "quiz_score" in s:
                quiz_scores.append(float(s["quiz_score"]))

        if quiz_scores:
            avg_quiz_score = sum(quiz_scores) / len(quiz_scores)

        return {
            "user_id": str(user_id),
            "lessons_generated": completed,
            "topics_completed_or_generated": topics,
            "avg_quiz_score": avg_quiz_score,
        }
