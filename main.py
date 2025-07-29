import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt
import pyfiglet

console = Console()
visited = []

def show_banner():
    banner = pyfiglet.figlet_format("DarkWeb Crawler")
    console.print(f"[bold green]{banner}[/bold green]")
    console.print("[magenta]Welcome to the darknet simulator.[/magenta]")
    console.print("Type [cyan]help[/cyan] to see available commands.\n")

def show_help():
    console.print("[bold yellow]Available commands:[/bold yellow]")
    console.print("  visit <url>     - Visit a darkweb page")
    console.print("  help            - Show this help message")
    console.print("  exit            - Exit the crawler")

def main_loop():
    while True:
        try:
            command = Prompt.ask(">>").strip().lower()
            if command == "help":
                show_help()
            elif command == "exit":
                console.print("[red]Exiting the crawler...[/red]")
                break
            elif command.startswith("visit"):
                console.print("[blue]Visit command coming soon...[/blue]")
            elif command == "":
                continue
            else:
                console.print(f"[red]Unknown command:[/red] {command}")
        except KeyboardInterrupt:
            console.print("\n[red]Exited by user.[/red]")
            break

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    show_banner()
    main_loop()
    