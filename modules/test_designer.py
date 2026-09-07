from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success
from utils.artifact_names import (
    TEST_CASES,
    REQUIREMENT_ANALYSIS,
)


class TestDesigner:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Designing test cases...")

        analysis = state.get_artifact(
            REQUIREMENT_ANALYSIS
        )

        if not analysis:
            raise ValueError(
                "Requirement Analysis artifact not found."
            )

        system_prompt = Path(
            "prompts/test_design_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        test_cases = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=analysis,
        )

        state.add_artifact(
            TEST_CASES,
            test_cases,
        )

        success("Test cases generated")

        return state