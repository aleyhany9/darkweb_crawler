import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt
import json
import base64
from rich.panel import Panel
from rich.text import Text
from time import sleep
import sys
import os

console = Console()
visited = []
os.makedirs("downloads", exist_ok=True)
found_flags = []

def resource_path(relative_path):
   
    if getattr(sys, 'frozen', False):
        
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def end_game_cinematic():
    console.clear()
    console.print(Panel.fit("[bold cyan]All flags captured.[/bold cyan]", border_style="green"))
    sleep(1.5)
    console.print(Panel.fit("[bold white]Decrypting core darknet systems...[/bold white]", border_style="cyan"))
    sleep(2)
    console.print(Panel.fit("[bold red]Bypassing hidden firewalls...[/bold red]", border_style="red"))
    sleep(2)
    console.print(Panel.fit("[bold green]Accessing final node: mainframe.hidden.onion[/bold green]", border_style="green"))
    sleep(2)
    console.print(Panel.fit("[bold magenta]FLAG DATABASE UNLOCKED![/bold magenta]", border_style="magenta"))
    sleep(2)

    console.print("\n")
    console.rule("[bold red]ENDGAME SEQUENCE INITIATED[/bold red]")

    outro_text = Text()
    outro_text.append("\nYou've reached the heart of the dark web.\n", style="bold cyan")
    outro_text.append("Every node. Every page. Every encrypted file.\n", style="bold white")
    outro_text.append("Decrypted. Owned. Controlled.\n\n", style="bold green")
    outro_text.append("You are now part of the system.\n", style="bold magenta")
    outro_text.append("Game Over. But the network remembers...\n", style="red")

    console.print(Panel(outro_text, border_style="bold blue"))
    sleep(3)
    console.print("\n[bold yellow]Thank you for playing the DarkWeb Crawler Simulator [/bold yellow]\n")

def show_banner():
    console.print("[magenta]Welcome to the darknet simulator.[/magenta]")
    console.print("Type [cyan]help[/cyan] to see available commands.\n")

def show_help():
    console.print("[bold yellow]Available commands:[/bold yellow]")
    console.print("  visit    <url>        - Visit a darkweb page")
    console.print("  decrypt  <filename>   - decrypt files based on type")
    console.print("  download <filename>   - download files")
    console.print("  instructions          - show you how to play this game")
    console.print("  decode                - to decode any content")
    console.print("  help                  - Show this help message")
    console.print("  exit                  - Exit the crawler")
    console.print("[red]        start with visit start.onion     [/red]")
    
def show_instructions():
    console.print("[bold cyan]How to Play:[/bold cyan]")
    console.print("- Start by visiting pages using: [green]visit <url>[/green]")
    console.print("- Explore hidden files and download them: [green]download <filename>[/green]")
    console.print("- Try decrypting the files: [green]decrypt <filename>[/green]")
    console.print("- Use clues in each page to find keys, links, or secrets.")
    console.print("- Your goal is to find all hidden flags across the network.\n")

import json
from pathlib import Path

save_file = Path(resource_path("darkweb_save.json"))

def save_game(current_url, visited, found_flags):
    state = {
        "current_url": current_url,
        "visited": list(visited),
        "flags": found_flags
    }
    with open(save_file, "w") as f:
        json.dump(state, f)


def download_file(filename):
    for url in visited:
        path = resource_path(f"content/{url}.json")
        with open(path, "r") as f:
            data = json.load(f)
            hidden = data.get("hidden_file")
            if hidden and hidden["name"] == filename:
                file_path = resource_path(os.path.join("downloads", filename))
                with open(file_path, "w") as out:
                    json.dump(hidden, out, indent=2)


                console.print(f"[green]✓ Downloaded {filename} to downloads/[/green]")
                return
    console.print(f"[red]File {filename} not found in visited pages.[/red]")            

def decrypt_file(filename):
    path = resource_path(os.path.join("downloads", filename))
    if not os.path.exists(path):
        console.print(f"[red]File not found: {filename}[/red]")
        return
    

    with open(path, "r") as f:
        try:
            file_data = json.load(f)
        except json.JSONDecodeError:
            console.print(f"[red]Invalid file format.[/red]")
            return
    ftype = file_data.get("type")
    if ftype == "encrypted_flag":
        user_key = Prompt.ask("[yellow]Enter decryption key[/yellow]")
        if user_key == file_data.get("key"):
            console.print(f"[bold green]Decryption successful![/bold green] Flag: [cyan]{file_data['flag']}[/cyan]")
        else:
            console.print("[red]Incorrect key.[/red]")
    elif ftype == "finalcheck":
        console.print("[bold cyan]You need to enter all 3 flags to finish the game.[/bold cyan]\n")

        entered_flags = []
        for i in range(1, 4):
            flag_input = Prompt.ask(f"[green]Enter Flag {i}[/green]").strip()
            entered_flags.append(flag_input)

        valid_flags = all(flag.startswith("FLAG{") and flag.endswith("}") for flag in entered_flags)

        if valid_flags:
            console.print("\n[bold lime]All flags look valid![/bold lime]")
            end_game_cinematic()
        else:
            console.print("[red]One or more flags are invalid. Try again.[/red]")


    elif ftype == "base64":
        try:
            decoded = base64.b64decode(file_data["content"]).decode()
            console.print(f"[bold green]Base64 Decoded:[/bold green] {decoded}")
        except:
            console.print("[red]Failed to decode base64.[/red]")
    elif ftype == "xor":
        xor_key = Prompt.ask("[yellow]Enter single character XOR key[/yellow]")
        try:
            if len(xor_key) != 1:
                console.print("[red]Please enter only a single character key.[/red]")
            else:
                encrypted = bytes.fromhex(file_data["content"])
                decrypted = ''.join(chr(b ^ ord(xor_key)) for b in encrypted)

                console.print(f"[bold green]XOR Decrypted:[/bold green] {decrypted}")

                if decrypted.startswith("FLAG{") and decrypted not in found_flags:
                    found_flags.append(decrypted)
                    save_game()
                    console.print("[bold cyan][✓] Flag found and saved![/bold cyan]")
                elif decrypted in found_flags:
                    console.print("[yellow]Flag already found.[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed XOR decryption.[/red] {e}")



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
                links = data.get("links", [])
                console.print(f"[bold yellow]Links:[/bold yellow] {', '.join(links) if links else 'None'}")

                if "hidden_file" in data:
                    file_info = data["hidden_file"]
                    console.print(f"[bold magenta]Hidden File Detected:[/bold magenta] {file_info['name']} ({file_info['type']})")

                print()   
            elif command == ("decrypt flag2.enc"):
                x = input("Enter decryption key:")
                if x == "K":
                    console.print("XOR Decrypted: [blue]FLAG{xor_hidden_flag}[/blue]") 
                else:
                    console.print("[red]you enter a wrong key [/red]")        
            elif command.startswith("download"):
                parts = command.split()
                if len(parts) != 2:
                    console.print("[red]Usage: download <filename>[/red]")
                    continue
                download_file(parts[1]) 
            elif command.startswith("decode"):
                console.print("[red][+] [/red] Decoded string: FLAG{base64_cruck}")
                console.print("[red]   visit finalcheck.onion to write the three flags [/red]")
            elif command == "instructions":
                show_instructions()    
            elif command.startswith("decrypt"):
                parts = command.split()
                if len(parts) != 2:
                    console.print("[red]Usage: decrypt <filename>[/red]")
                    continue
                decrypt_file(parts[1])
            elif command == "end":
                end_game_cinematic()    
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
    