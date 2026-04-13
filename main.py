"""
Common Notary Apostille — Customer Service Head Bot
Entry point for the CLI chat interface.

Usage:
    python main.py                  # Start customer chat session
    python main.py --operator       # Start in operator mode (can request email drafts, etc.)

Setup:
    1. Copy .env.example to .env and fill in your ANTHROPIC_API_KEY
    2. pip install -r requirements.txt
    3. python main.py
"""

import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt
from rich.markdown import Markdown

from config.settings import COMPANY_NAME, COMPANY_EMAIL, COMPANY_PHONE, ANTHROPIC_API_KEY
from agents.head_bot import HeadBot

console = Console()

BANNER = f"""
╔══════════════════════════════════════════════════════════════╗
║          {COMPANY_NAME.center(50)}          ║
║              Customer Service — Powered by AI                ║
╚══════════════════════════════════════════════════════════════╝
"""

OPERATOR_COMMANDS = """
[bold cyan]Operator Commands:[/bold cyan]
  [bold]/new[/bold]         — Start a new customer session (clears history)
  [bold]/email[/bold]       — Request an email draft for the current customer
  [bold]/context[/bold]     — Show what the bot knows about the current customer
  [bold]/quit[/bold]        — Exit the program
"""

CUSTOMER_COMMANDS = """
  Type your question and press Enter.
  Type [bold]/quit[/bold] to exit.
"""


def check_api_key() -> None:
    """Verify that an API key is configured before starting."""
    if not ANTHROPIC_API_KEY:
        console.print(
            Panel(
                "[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY is not set.\n\n"
                "1. Copy [bold].env.example[/bold] to [bold].env[/bold]\n"
                "2. Add your Anthropic API key to the .env file\n"
                "3. Run the program again",
                title="Configuration Required",
                border_style="red",
            )
        )
        sys.exit(1)


def print_banner(operator_mode: bool) -> None:
    """Print the startup banner."""
    console.print(f"[bold blue]{BANNER}[/bold blue]")
    mode_label = "[bold yellow]OPERATOR MODE[/bold yellow]" if operator_mode else "[bold green]CUSTOMER MODE[/bold green]"
    console.print(f"  Mode: {mode_label}")
    if COMPANY_EMAIL:
        console.print(f"  Contact: {COMPANY_EMAIL}", style="dim")
    if COMPANY_PHONE:
        console.print(f"  Phone:   {COMPANY_PHONE}", style="dim")
    console.print()


def print_help(operator_mode: bool) -> None:
    """Print usage hints."""
    if operator_mode:
        console.print(Panel(OPERATOR_COMMANDS, border_style="cyan"))
    else:
        console.print(Panel(CUSTOMER_COMMANDS, border_style="green"))


def format_bot_response(response: str) -> None:
    """Display the bot's response with nice formatting."""
    console.print()
    console.print(
        Panel(
            Markdown(response),
            title=f"[bold blue]{COMPANY_NAME}[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
    )
    console.print()


def show_context(bot: HeadBot) -> None:
    """Display the current customer context in operator mode."""
    ctx = bot.customer_context
    lines = []
    for key, value in ctx.items():
        if value:
            lines.append(f"  [cyan]{key}:[/cyan] {value}")
    if lines:
        console.print(Panel("\n".join(lines), title="Current Customer Context", border_style="yellow"))
    else:
        console.print("[dim]No customer context gathered yet.[/dim]")


def run_operator_email_request(bot: HeadBot) -> None:
    """Interactive email draft request in operator mode."""
    console.print("[bold cyan]Email Draft Request[/bold cyan]")
    customer_name = Prompt.ask("  Customer name", default="Valued Customer")
    instructions = Prompt.ask("  What should the email accomplish?")

    message = (
        f"Please draft an email for a customer named {customer_name}. "
        f"Instructions: {instructions}"
    )
    console.print("\n[dim]Generating email draft...[/dim]\n")
    response = bot.chat(message)
    format_bot_response(response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"{COMPANY_NAME} Customer Service Head Bot"
    )
    parser.add_argument(
        "--operator",
        action="store_true",
        help="Run in operator mode (access to email drafts and session commands)",
    )
    args = parser.parse_args()
    operator_mode = args.operator

    check_api_key()
    print_banner(operator_mode)
    print_help(operator_mode)

    bot = HeadBot()

    # Auto-greet the customer on first launch in customer mode
    if not operator_mode:
        console.print("[dim]Connecting you to our customer service team...[/dim]\n")
        greeting = bot.chat(
            "A new customer has just started a chat session. Please greet them warmly, "
            "introduce Common Notary Apostille, and ask how you can help them today."
        )
        format_bot_response(greeting)

    # Main chat loop
    while True:
        try:
            if operator_mode:
                user_input = Prompt.ask("[bold yellow]Operator[/bold yellow]").strip()
            else:
                user_input = Prompt.ask("[bold green]You[/bold green]").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
                console.print("\n[dim]Thank you for using Common Notary Apostille. Goodbye![/dim]\n")
                break

            if operator_mode:
                if user_input.lower() == "/new":
                    bot.reset()
                    console.print(Rule("[dim]New customer session started[/dim]"))
                    continue

                if user_input.lower() == "/context":
                    show_context(bot)
                    continue

                if user_input.lower() == "/email":
                    run_operator_email_request(bot)
                    continue

                if user_input.lower() == "/help":
                    print_help(operator_mode)
                    continue

            # Send message to Head Bot
            console.print("[dim]Processing...[/dim]")
            response = bot.chat(user_input)
            format_bot_response(response)

        except KeyboardInterrupt:
            console.print("\n\n[dim]Session interrupted. Goodbye![/dim]\n")
            break
        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]An error occurred:[/bold red] {str(e)}\n\n"
                    "Please try again or contact support.",
                    border_style="red",
                )
            )


if __name__ == "__main__":
    main()
