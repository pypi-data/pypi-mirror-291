from rich.console import Console
from time import sleep
import random

console = Console()

sus_animations = [
    "Checking for impostors...",
    "Scanning vents... nothing found.",
    "Analyzing suspicious files...",
    "Red alert! Something feels off...",
    "Verifying crew members...",
    "Someone vented... stay alert!",
    "Is that an impostor? Nah, just a bug.",
    "Crewmate spotted... but are they trustworthy?",
    "Running diagnostics... results inconclusive.",
    "Emergency meeting... who's the impostor?",
    "Electrical seems sus... proceed with caution.",
    "Scanning files... did I see a sussy baka?",
    "Uploading files... hopefully, no impostors!",
    "Monitoring systems... all seems quiet. Too quiet.",
    "Inspecting data... something's not adding up.",
    "Checking for anomalies... stay vigilant!",
    "This system is looking kinda sus...",
    "Crewmates behaving strangely... better watch out.",
    "Are those wires crossed? Might be sabotage.",
    "Did I just see someone fake a task?",
    "Shields are down... better fix that before someone notices.",
]


def animate_sus_art(level: int):
    for _ in range(level):
        console.print(f"[bold yellow]{random.choice(sus_animations)}[/bold yellow]")
        sleep(1)
