from pathlib import Path

from utils.ai_client import AIClient


class RequirementAnalyzer:

    def run(self, state):

        print("1. Reading specification...")

        specification = Path(
            "specifications/login.md"
        ).read_text(
            encoding="utf-8"
        )

        print("2. Specification loaded")

        state.add_artifact(
            "specification",
            specification,
        )

        system_prompt = Path(
            "prompts/requirement_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        print("3. Prompt loaded")

        ai = AIClient()

        print("4. Calling Ollama...")

        analysis = ai.generate(
            system_prompt=system_prompt,
            user_prompt=specification,
        )

        print("5. AI response received")

        state.add_artifact(
            "analysis",
            analysis,
        )

        print("6. Analysis saved")

        return state