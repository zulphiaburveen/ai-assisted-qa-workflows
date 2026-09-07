from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success
from utils.artifact_names import (
    SPECIFICATION,
    REQUIREMENT_ANALYSIS,
)


class RequirementAnalyzer:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Reading specification...")

        specification = Path(
            "specifications/login.md"
        ).read_text(
            encoding="utf-8"
        )

        state.add_artifact(
            SPECIFICATION,
            specification,
        )

        success("Specification loaded")

        system_prompt = Path(
            "prompts/requirement_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        success("Requirement prompt loaded")

        step("Analysing requirements...")

        analysis = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=specification,
        )

        state.add_artifact(
            REQUIREMENT_ANALYSIS,
            analysis,
        )

        success("Requirement analysis generated")

        return state