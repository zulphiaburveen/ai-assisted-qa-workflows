from pathlib import Path

from utils.ai_client import AIClient
from utils.logger import step, success

from utils.artifact_names import (
    TEST_SCENARIOS,
    TEST_EVALUATION,
    PLAYWRIGHT_AUTOMATION,
)


class AutomationGenerator:

    def __init__(self):
        self.ai = AIClient()

    def run(self, state):

        step("Generating Playwright automation...")

        scenarios = state.get_artifact(TEST_SCENARIOS)
        evaluation = state.get_artifact(TEST_EVALUATION)

        if not scenarios:
            raise ValueError("Test Scenarios artifact not found.")

        if not evaluation:
            raise ValueError("Test Evaluation artifact not found.")

        system_prompt = Path(
            "prompts/automation_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        # Try to use representative scenarios from the evaluation.
        # If they don't exist yet, fall back to two fixed demo scenarios.
        marker = "# Representative Automation Scenarios"

        if marker in evaluation:
            representative = evaluation.split(marker, 1)[1].strip()
        else:
            representative = """
## FT-001 – Valid Login

- Navigate to https://www.saucedemo.com
- Login using:
  - Username: standard_user
  - Password: secret_sauce
- Verify the Products page is displayed.

---

## UX-001 – Swag Labs Heading

Verify:

- Swag Labs logo is visible.
- Text is "Swag Labs".
- Font family matches the specification.
- Font size matches the specification.
- Font weight matches the specification.
"""

        user_prompt = f"""
Generate Playwright automation ONLY for the following representative scenarios.

The output MUST contain exactly TWO Playwright tests.

{representative}
"""

        playwright = self.ai.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        playwright = (
            playwright
            .replace("```typescript", "")
            .replace("```ts", "")
            .replace("```", "")
            .strip()
        )

        import_line = "import { test, expect } from '@playwright/test';"

        if not playwright.startswith(import_line):
            playwright = f"{import_line}\n\n{playwright}"

        state.add_artifact(
            PLAYWRIGHT_AUTOMATION,
            playwright,
        )

        success("Playwright automation generated")

        # Copy into Playwright project
        playwright_test = Path("playwright/tests/generated.spec.ts")

        playwright_test.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        playwright_test.write_text(
            playwright,
            encoding="utf-8",
        )

        success(f"Playwright test copied to {playwright_test}")

        return state