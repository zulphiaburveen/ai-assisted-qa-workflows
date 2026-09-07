from ollama import chat

from utils.logger import ai, success


class AIClient:

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        ai("Thinking...")

        response = chat(
            model="qwen3:latest",
            think=False,
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

        success("AI response received")

        return response.message.content