from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success

from utils.artifact_names import (
    REQUIREMENT_ANALYSIS,
    TEST_SCENARIOS,
    TEST_EVALUATION,
)


class TestEvaluator:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Evaluating test scenarios...")

        analysis = state.get_artifact(REQUIREMENT_ANALYSIS)
        scenarios = state.get_artifact(TEST_SCENARIOS)

        if not analysis:
            raise ValueError("Requirement Analysis artifact not found.")

        if not scenarios:
            raise ValueError("Test Scenarios artifact not found.")

        system_prompt = Path(
            "prompts/evaluation_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        user_prompt = f"""
Requirement Analysis

{analysis}

--------------------------------

Test Scenarios

{scenarios}
"""

        evaluation = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        state.add_artifact(
            TEST_EVALUATION,
            evaluation,
        )

        success("Test evaluation generated")

        return state