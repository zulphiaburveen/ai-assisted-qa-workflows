import os
import time
import argparse

os.system("chcp 65001 > nul")

from rich.console import Console
from rich.table import Table

from utils.workflow_state import WorkflowState
from utils.logger import step, success

from modules.requirement_analyzer import RequirementAnalyzer
from modules.test_designer import TestDesigner
from modules.test_evaluator import TestEvaluator
from modules.automation_generator import AutomationGenerator
from modules.playwright_runner import PlaywrightRunner
from modules.automation_reviewer import AutomationReviewer

from utils.artifact_names import (
    REQUIREMENT_ANALYSIS,
    TEST_SCENARIOS,
    TEST_EVALUATION,
    PLAYWRIGHT_AUTOMATION,
    PLAYWRIGHT_RESULTS,
    AUTOMATION_REVIEW,
)

parser = argparse.ArgumentParser()

parser.add_argument(
    "--profile",
    choices=["full", "demo"],
    default="full",
)

args = parser.parse_args()

console = Console()

console.print("[bold green]AI Assisted QA Workflow[/bold green]")
console.print()

state = WorkflowState()

# ---------------------------------------------------------
# Demo Mode - Load existing artifacts from disk
# ---------------------------------------------------------

from pathlib import Path

if args.profile == "demo":

    console.print("[bold yellow]Loading existing artifacts...[/bold yellow]")

    artifact_files = {
        REQUIREMENT_ANALYSIS: "artifacts/02_requirement_analysis.md",
        TEST_SCENARIOS: "artifacts/03_test_scenarios.md",
        TEST_EVALUATION: "artifacts/04_test_evaluation.md",
    }

    for artifact, file_path in artifact_files.items():

        path = Path(file_path)

        if path.exists():
            state.add_artifact(
                artifact,
                path.read_text(encoding="utf-8"),
            )
            success(f"Loaded {path.name}")
        else:
            console.print(f"[red]Missing {path}[/red]")

# ---------------------------------------------------------

PIPELINE = [
    ("requirement-analyzer", "Requirement Analyzer", RequirementAnalyzer()),
    ("test-designer", "Test Designer", TestDesigner()),
    ("test-evaluator", "Test Evaluator", TestEvaluator()),
    ("generator", "Automation Generator", AutomationGenerator()),
    ("playwright-runner", "Playwright Runner", PlaywrightRunner()),
    ("automation-reviewer", "Automation Reviewer", AutomationReviewer()),
]

if args.profile == "demo":
    start_from = "generator"
    console.print("[bold yellow]Running in DEMO mode[/bold yellow]\n")
else:
    start_from = "requirement-analyzer"
    console.print("[bold cyan]Running in FULL mode[/bold cyan]\n")

step("Starting workflow")

start = False
module_times = []

for key, name, module in PIPELINE:

    if key == start_from:
        start = True

    if not start:
        success(f"Skipping {name}")
        continue

    start_time = time.perf_counter()

    state = module.run(state)

    elapsed = time.perf_counter() - start_time

    module_times.append((name, elapsed))

    success(f"{name} completed ({elapsed:.2f}s)")

console.print()

timing_table = Table(title="Module Timing Summary")

timing_table.add_column("Module", style="cyan")
timing_table.add_column("Time", justify="right")

total = 0

for name, elapsed in module_times:
    timing_table.add_row(name, f"{elapsed:.2f}s")
    total += elapsed

timing_table.add_row(
    "[bold]Total[/bold]",
    f"[bold]{total:.2f}s[/bold]",
)

console.print(timing_table)

artifact_table = Table(title="Generated Artifacts")

artifact_table.add_column("Artifact")

artifacts = [
    REQUIREMENT_ANALYSIS,
    TEST_SCENARIOS,
    TEST_EVALUATION,
    PLAYWRIGHT_AUTOMATION,
    PLAYWRIGHT_RESULTS,
    AUTOMATION_REVIEW,
]

for artifact in artifacts:
    if state.get_artifact(artifact):
        artifact_table.add_row(f"✓ {artifact}")

console.print()
console.print(artifact_table)

console.print()
console.print("[bold green]Workflow completed successfully.[/bold green]")