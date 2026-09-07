from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success

from utils.artifact_names import (
    REQUIREMENT_ANALYSIS,
    TEST_CASES,
    TEST_EVALUATION,
)


class TestEvaluator:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Evaluating automation scenarios...")

        analysis = state.get_artifact(REQUIREMENT_ANALYSIS)
        scenarios = state.get_artifact(TEST_CASES)

        system_prompt = Path(
            "prompts/test_evaluation_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        prompt = f"""
Requirement Analysis

{analysis}

--------------------------------

Automation Scenarios

{scenarios}
"""

        evaluation = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )

        state.add_artifact(
            TEST_EVALUATION,
            evaluation,
        )

        success("Test evaluation generated")

        return state