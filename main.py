import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt
import pyfiglet
import json

console = Console()
visited = []
os.makedirs("downloads", exist_ok=True)

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

def download_file(filename):
    for url in visited:
        path = f"content/{url}.json"
        with open(path, "r") as f:
            data = json.load(f)
            hidden = data.get("hidden_file")
            if hidden and hidden["name"] == filename:
                file_path = os.path.join("downloads", filename)
                with open(file_path, "w") as out:
                    out.write("ENCRYPTED DATA PLACEHOLDER")

                console.print(f"[green]✓ Downloaded {filename} to downloads/[/green]")
                return
    console.print(f"[red]File {filename} not found in visited pages.[/red]")            

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
                parts = command.split()
                if len(parts) != 2:
                    console.print("[red]Usage: visit <url>[/red]")
                    continue

                url = parts[1]
                path = f"content/{url}.json"

                if not os.path.exists(path):
                    console.print(f"[red]No page found for {url}[/red]")
                    continue
                
                import json
                with open(path, "r") as f:
                    data = json.load(f)

                if url not in visited:
                    visited.append(url)

                console.print(f"\n[bold green]Visiting: {data['url']}[/bold green]")
                console.print(f"[cyan]Title:[/cyan] {data['title']}")
                console.print(f"[dim]Content:[/dim] {data['content']}")
                console.print(f"[bold yellow]Links:[/bold yellow] {', '.join(data['links']) or 'None'}")

                if "hidden_file" in data:
                    file_info = data["hidden_file"]
                    console.print(f"[bold magenta]Hidden File Detected:[/bold magenta] {file_info['name']} ({file_info['type']})")

                print()    
            elif command.startswith("download"):
                parts = command.split()
                if len(parts) != 2:
                    console.print("[red]Usage: download <filename>[/red]")
                    continue
                download_file(parts[1])

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
    