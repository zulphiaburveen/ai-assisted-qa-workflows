from pathlib import Path
import shutil
import subprocess

from utils.logger import step, success
from utils.artifact_names import PLAYWRIGHT_RESULTS


class PlaywrightRunner:

    def run(self, state):

        step("Running Playwright tests...")

        project_dir = Path("playwright").resolve()

        npm = shutil.which("npm.cmd") or shutil.which("npm")

        if not npm:
            raise RuntimeError("npm.cmd not found in PATH")

        print(f"Project directory: {project_dir}")
        print(f"Project exists: {project_dir.exists()}")
        print(f"npm: {npm}")

        result = subprocess.run(
            [
                npm,
                "exec",
                "--",
                "playwright",
                "test",
                "--reporter=list",
                "tests/generated.spec.ts",
            ],
            cwd=project_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        execution_output = result.stdout

        if result.stderr:
            execution_output += "\n\n" + result.stderr

        state.add_artifact(
            PLAYWRIGHT_RESULTS,
            execution_output,
        )

        print(execution_output)

        print(f"Playwright results length: {len(execution_output)}")

        if result.returncode == 0:
            success("Playwright tests passed")
        else:
            print("⚠️ Playwright tests completed with failures.")
            print("Continuing workflow for AI Automation Review...")

        return state