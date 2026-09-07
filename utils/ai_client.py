from ollama import chat


class AIClient:

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        print("🤖 AI is analysing requirements...")

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

        print("✓ Requirement Analysis Complete")

        return response.message.content