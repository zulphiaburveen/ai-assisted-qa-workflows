from pathlib import Path


class RequirementAnalyzer:

    def run(self, state):

        specification = Path("specifications/login.md").read_text(
            encoding="utf-8"
        )

        state.add_artifact("specification", specification)

        analysis = """
# Requirement Analysis

## Missing Requirements
- Session timeout
- Password expiry

## Risk Level
Medium
"""

        state.add_artifact("analysis", analysis)

        return state