import os
import json
from dotenv import load_dotenv

load_dotenv()


class AIContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "demo_key")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1500"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.demo_mode = (self.api_key == "demo_key")

    def generate_personalized_content(self, user_profile, topic):
        """
        Generate personalized training content based on user profile.

        Args:
            user_profile: User profile dictionary
            topic: Training topic (e.g., 'phishing', 'password_security')

        Returns:
            Personalized lesson content as string
        """
        if self.demo_mode:
            return self._generate_demo_content(user_profile, topic)
        else:
            # Real API path (kept here for completeness, but lab uses demo_key)
            # This code will only run if a real key is provided.
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)

                prompt = self._build_prompt(user_profile, topic)

                resp = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity training content generator."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                return resp.choices[0].message.content
            except Exception as e:
                return f"[ERROR calling AI API] {e}\n\nFalling back to demo content:\n\n{self._generate_demo_content(user_profile, topic)}"

    def _build_prompt(self, user_profile, topic):
        name = user_profile.get("name", "Student")
        exp = user_profile.get("experience_level", "beginner")
        style = user_profile.get("learning_style", "visual")
        interests = user_profile.get("interests", [])
        interests_str = ", ".join(interests) if interests else "general cybersecurity"

        return (
            f"Create a personalized cybersecurity lesson.\n"
            f"User: {name}\n"
            f"Experience level: {exp}\n"
            f"Learning style: {style}\n"
            f"Interests: {interests_str}\n"
            f"Topic: {topic}\n\n"
            "Lesson requirements:\n"
            "- Use simple headings\n"
            "- Include practical examples\n"
            "- Include actionable checklist\n"
            "- End with a short recap\n"
        )

    def _generate_demo_content(self, user_profile, topic):
        """Generate demo content for lab purposes."""
        experience = user_profile.get("experience_level", "beginner")
        name = user_profile.get("name", "Student")
        learning_style = user_profile.get("learning_style", "visual")
        interests = user_profile.get("interests", [])

        topic_title = topic.replace("_", " ").title()
        interests_str = ", ".join(interests) if interests else "general cybersecurity"

        # Content templates for different experience levels
        if experience == "beginner":
            intro = (
                f"Hi {name}! This lesson introduces **{topic_title}** in a simple and practical way.\n"
                "You will learn the basics and how to stay safe in everyday situations."
            )
            key_concepts = [
                "What it is (simple definition)",
                "Why it matters",
                "Common examples you might see",
                "One or two easy rules to remember",
            ]
            difficulty_note = "Keep it simple and focus on habits you can apply today."
        elif experience == "intermediate":
            intro = (
                f"Hi {name}! This lesson covers **{topic_title}** with real examples and best practices.\n"
                "You already know the basics, so we will focus on stronger decision-making and patterns."
            )
            key_concepts = [
                "Core concepts and common attack patterns",
                "How attackers exploit human behavior",
                "How to verify and respond safely",
                "Common mistakes and how to avoid them",
            ]
            difficulty_note = "Use practical scenarios and stronger best practices."
        else:
            intro = (
                f"Hi {name}! This advanced lesson explores **{topic_title}** with deeper security reasoning.\n"
                "We will focus on threat models, edge cases, and how to improve organizational controls."
            )
            key_concepts = [
                "Threat model and attacker goals",
                "Advanced detection and prevention techniques",
                "Policy and control mapping",
                "How to measure and improve security outcomes",
            ]
            difficulty_note = "Include advanced scenarios and control recommendations."

        # Customize content based on learning style
        if learning_style == "visual":
            examples = [
                "Look for visual red flags (odd sender domain, mismatched URLs, unusual formatting).",
                "Use screenshots and checklists to compare safe vs unsafe examples.",
            ]
            practice = "Practice by reviewing 3 examples and marking red flags you see."
        elif learning_style == "auditory":
            examples = [
                "Explain the scenario out loud and describe why it is suspicious.",
                "Use short spoken summaries after each section to reinforce learning.",
            ]
            practice = "Practice by explaining the safe response steps to a colleague or recording a short voice note."
        elif learning_style == "kinesthetic":
            examples = [
                "Do a hands-on simulation: inspect headers, hover links, report suspicious messages.",
                "Use an interactive exercise where you choose actions step-by-step.",
            ]
            practice = "Practice by completing a simulated scenario and documenting your actions."
        else:
            examples = [
                "Read a short case study and highlight key signals.",
                "Write down response steps and create a personal checklist.",
            ]
            practice = "Practice by writing a 5-step response plan and using it for sample cases."

        content = f"""
# {topic_title} Training for {name}

## Introduction
{intro}

## Key Concepts
- {key_concepts[0]}
- {key_concepts[1]}
- {key_concepts[2]}
- {key_concepts[3]}

## Practical Examples (Tailored to {learning_style} learning style)
- {examples[0]}
- {examples[1]}

## Action Items (Based on your interests: {interests_str})
1. Apply one safe habit today related to {topic_title}.
2. Share one learning point with your team or peer group.
3. Add a reminder/checklist in your daily workflow.

## Practice Activity
{practice}

## Notes on Difficulty
{difficulty_note}

## Quick Recap
- {topic_title} matters because it reduces real-world risk.
- Use safe verification steps before trusting messages or actions.
- Consistent habits beat one-time awareness.
"""
        return content.strip()

    def generate_quiz(self, user_profile, topic, num_questions=5):
        """
        Generate personalized quiz questions.
        """
        experience = user_profile.get("experience_level", "beginner")
        learning_style = user_profile.get("learning_style", "visual")
        name = user_profile.get("name", "Student")

        topic_title = topic.replace("_", " ").title()

        # Adjust difficulty by experience
        if experience == "beginner":
            difficulty = "easy"
        elif experience == "intermediate":
            difficulty = "medium"
        else:
            difficulty = "hard"

        questions = []
        for i in range(1, num_questions + 1):
            if difficulty == "easy":
                q = {
                    "question": f"[{topic_title}] Q{i}: Which is a safe first step when you suspect a {topic_title.lower()} issue?",
                    "options": [
                        "Click quickly to see what happens",
                        "Ignore it completely",
                        "Verify using a trusted method and report if needed",
                        "Share it widely to warn everyone immediately",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Verification and reporting are safe first steps.",
                }
            elif difficulty == "medium":
                q = {
                    "question": f"[{topic_title}] Q{i}: Which signal is most reliable for identifying risk in a realistic scenario?",
                    "options": [
                        "Message looks urgent",
                        "Sender domain and link destination do not match trusted sources",
                        "It uses friendly language",
                        "It includes a company logo",
                    ],
                    "correct_answer_index": 1,
                    "explanation": "Technical mismatch (domain/link) is a strong indicator of risk.",
                }
            else:
                q = {
                    "question": f"[{topic_title}] Q{i}: Which control best reduces organizational risk related to {topic_title.lower()}?",
                    "options": [
                        "Rely only on user caution",
                        "Disable all email usage",
                        "Layered controls (MFA, filtering, awareness, reporting) with monitoring",
                        "Only update policies once per year",
                    ],
                    "correct_answer_index": 2,
                    "explanation": "Layered controls and monitoring reduce risk more effectively than single controls.",
                }

            # Slight personalization mention
            q["personalization_note"] = f"User: {name}, Style: {learning_style}, Difficulty: {difficulty}"
            questions.append(q)

        return questions
