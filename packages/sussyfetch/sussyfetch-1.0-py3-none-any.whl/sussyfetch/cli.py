import argparse
from sussyfetch.system_info import get_system_info
from sussyfetch.sus_phrases import get_sus_info
from sussyfetch.ascii_art import display_ascii_art
from sussyfetch.animations import animate_sus_art

from rich.console import Console

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Sussyfetch: Suspiciously Fetching System Info"
    )
    parser.add_argument(
        "--sus-level", type=int, help="Level of sussiness (1-10)", default=5
    )
    args = parser.parse_args()

    # Display ASCII art with animation
    display_ascii_art()
    # Display a sus phrase based on the sus level
    sus_phrase = get_sus_info(args.sus_level)
    console.print(
        f"[bold red]Suspicion Level {args.sus_level}: {sus_phrase}[/bold red]"
    )

    animate_sus_art(args.sus_level)

    console.print("[bold green]Done![/bold green]")

    # Fetch and display system info
    get_system_info()
    # for key, value in sys_info.items():
    #     print(f"{key}: {value}")


if __name__ == "__main__":
    main()
