from datetime import datetime

from src.user_profile import UserProfileManager
from src.training_manager import TrainingManager
from src.audio_manager import AudioManager


class PersonalizedTrainingSystem:
    def __init__(self):
        self.profile_manager = UserProfileManager()
        self.training_manager = TrainingManager()
        self.audio_manager = AudioManager()

    def onboard_user(self, user_id, name, experience, learning_style, interests):
        """
        Onboard new user and create profile.

        Returns:
            Created profile and recommended learning path
        """
        profile = self.profile_manager.create_profile(
            user_id=user_id,
            name=name,
            experience_level=experience,
            learning_style=learning_style,
            interests=interests,
        )

        learning_path = self.training_manager.generate_learning_path(user_id)

        return {
            "profile": profile,
            "recommended_learning_path": learning_path,
        }

    def deliver_lesson(self, user_id, topic, include_audio=True):
        """
        Deliver complete personalized lesson with optional audio.
        """
        lesson = self.training_manager.create_personalized_lesson(user_id, topic)

        audio_meta = None
        if include_audio:
            audio_meta = self.audio_manager.create_lesson_audio(
                lesson_id=lesson["lesson_id"],
                lesson_content=lesson["content"],
                preferences={"engine": "offline"},
            )

        bundle = {
            "lesson": lesson,
            "audio": audio_meta,
        }

        return bundle

    def track_progress(self, user_id, lesson_id, quiz_score):
        """
        Track user progress and update profile.
        """
        profile = self.profile_manager.get_profile(user_id)
        if not profile:
            raise ValueError(f"User profile not found: {user_id}")

        completed = profile.get("completed_modules", [])
        if lesson_id not in completed:
            completed.append(lesson_id)

        quiz_history = profile.get("quiz_history", [])
        quiz_history.append(
            {
                "lesson_id": lesson_id,
                "score": quiz_score,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

        updated = self.profile_manager.update_profile(
            user_id,
            {"completed_modules": completed, "quiz_history": quiz_history},
        )
        return updated

    def generate_report(self, user_id):
        """
        Generate progress report for user.
        """
        profile = self.profile_manager.get_profile(user_id)
        if not profile:
            raise ValueError(f"User profile not found: {user_id}")

        progress = self.training_manager.get_user_progress(user_id)

        quiz_history = profile.get("quiz_history", [])
        avg_quiz = None
        if quiz_history:
            scores = [float(x.get("score", 0)) for x in quiz_history]
            avg_quiz = sum(scores) / len(scores)

        recommendations = []
        if avg_quiz is not None and avg_quiz < 70:
            recommendations.append("Consider reviewing lessons again and taking quizzes after practice.")
        if not profile.get("completed_modules"):
            recommendations.append("Start with the first topic in your learning path to build momentum.")
        if profile.get("experience_level") == "beginner":
            recommendations.append("Focus on phishing + password safety first for maximum risk reduction.")

        return {
            "user_id": str(user_id),
            "profile_summary": {
                "name": profile.get("name"),
                "experience_level": profile.get("experience_level"),
                "learning_style": profile.get("learning_style"),
                "interests": profile.get("interests", []),
            },
            "progress": progress,
            "avg_quiz_score": avg_quiz,
            "recommendations": recommendations,
        }
