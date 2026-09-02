from rich.console import Console

from utils.workflow_state import WorkflowState
from modules.requirement_analyzer import RequirementAnalyzer

console = Console()

console.print("[bold green]AI Assisted QA Workflow[/bold green]")

state = WorkflowState()

console.print("Loading Specification...")

state = RequirementAnalyzer().run(state)

console.print("[green]✓ Analysis Generated[/green]")

console.print("Analysis saved to artifacts/analysis.md")