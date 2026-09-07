from rich.console import Console
from rich.panel import Panel

console = Console()


def step(message: str):
    console.print(f"[cyan]▶ {message}[/cyan]")


def ai(message: str):
    console.print(f"[magenta]🤖 {message}[/magenta]")


def success(message: str):
    console.print(f"[green]✓ {message}[/green]")


def panel(title: str, body: str):
    console.print(
        Panel(
            body,
            title=title,
            expand=False,
        )
    )