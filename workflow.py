from rich.console import Console
import time

from utils.workflow_state import WorkflowState
from utils.logger import step, success

from modules.requirement_analyzer import RequirementAnalyzer
from modules.test_designer import TestDesigner

console = Console()

console.print("[bold green]AI Assisted QA Workflow[/bold green]")
console.print()

state = WorkflowState()

PIPELINE = [
    ("Requirement Analyzer", RequirementAnalyzer()),
    ("Test Designer", TestDesigner()),
]

step("Starting workflow")

for name, module in PIPELINE:

    start = time.perf_counter()

    state = module.run(state)

    elapsed = time.perf_counter() - start

    success(f"{name} completed ({elapsed:.2f}s)")

console.print()
console.print("[bold green]Workflow completed successfully.[/bold green]")