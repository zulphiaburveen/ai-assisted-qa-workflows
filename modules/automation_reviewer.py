from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success
from utils.artifact_names import (
    PLAYWRIGHT_AUTOMATION,
    PLAYWRIGHT_RESULTS,
    AUTOMATION_REVIEW,
)


class AutomationReviewer:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Reviewing Playwright automation...")

        automation = state.get_artifact(PLAYWRIGHT_AUTOMATION)
        results = state.get_artifact(PLAYWRIGHT_RESULTS)

        print(f"Automation length: {len(automation) if automation else 0}")
        print(f"Results length: {len(results) if results else 0}")

        if not automation:
            raise ValueError("Playwright Automation artifact not found.")

        if not results:
            raise ValueError("Playwright Results artifact not found.")

        system_prompt = Path(
            "prompts/automation_review_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        user_prompt = f"""
Review the following Playwright automation and execution results.

## Playwright Automation

{automation[:2000]}

--------------------------------

## Playwright Execution Results

{results[-2500:]}
"""

        review = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        print(f"Review length: {len(review)}")

        state.add_artifact(
            AUTOMATION_REVIEW,
            review,
        )

        success("Automation review generated")

        return state