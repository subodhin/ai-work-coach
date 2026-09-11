import os

from mistralai.client import Mistral

from .base import LLMProvider


class MistralProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError("MISTRAL_API_KEY not configured")

        self.client = Mistral(api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> str:

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content