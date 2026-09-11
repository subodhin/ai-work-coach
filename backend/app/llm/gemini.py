
import os

from google import genai

from .base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite",
        )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"""
SYSTEM INSTRUCTIONS:

{system_prompt}

USER REQUEST:

{user_prompt}
""",
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response")

        return response.text

