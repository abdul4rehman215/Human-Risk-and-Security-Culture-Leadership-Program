import json
import os
from datetime import datetime


class UserProfileManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.profiles_file = os.path.join(data_dir, "profiles.json")
        os.makedirs(data_dir, exist_ok=True)

    def create_profile(self, user_id, name, experience_level, learning_style, interests):
        """
        Create a new user profile with personalization attributes.

        Args:
            user_id: Unique identifier
            name: User's name
            experience_level: beginner, intermediate, or advanced
            learning_style: visual, auditory, kinesthetic, or reading
            interests: List of cybersecurity topics

        Returns:
            Created profile dictionary
        """
        profiles = self.load_profiles()

        now = datetime.utcnow().isoformat() + "Z"

        profile = {
            "user_id": str(user_id),
            "name": str(name),
            "experience_level": str(experience_level).lower().strip(),
            "learning_style": str(learning_style).lower().strip(),
            "interests": interests if isinstance(interests, list) else [str(interests)],
            "completed_modules": [],
            "quiz_history": [],
            "created_at": now,
            "last_updated": now,
        }

        profiles[str(user_id)] = profile
        self.save_profiles(profiles)
        return profile

    def load_profiles(self):
        """Load all profiles from JSON file."""
        if not os.path.exists(self.profiles_file):
            return {}
        try:
            with open(self.profiles_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except json.JSONDecodeError:
            # If file is corrupted, return empty safely
            return {}
        except Exception:
            return {}

    def save_profiles(self, profiles):
        """Save profiles to JSON file."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.profiles_file, "w") as f:
            json.dump(profiles, f, indent=2)

    def get_profile(self, user_id):
        """Retrieve specific user profile."""
        profiles = self.load_profiles()
        return profiles.get(str(user_id))

    def update_profile(self, user_id, updates):
        """Update existing profile with new data."""
        profiles = self.load_profiles()
        uid = str(user_id)

        if uid not in profiles:
            return None

        profile = profiles[uid]

        # Apply updates
        if isinstance(updates, dict):
            for k, v in updates.items():
                profile[k] = v

        profile["last_updated"] = datetime.utcnow().isoformat() + "Z"
        profiles[uid] = profile

        self.save_profiles(profiles)
        return profile
