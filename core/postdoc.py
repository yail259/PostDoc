#!/usr/bin/env python3
"""
POSTDOC CLI Tool

This script generates documentation for a codebase or single file using OpenAI's API.
It can load settings from a YAML config file or interactively prompt the user.
It also respects your .gitignore patterns when collecting code.
"""

import os
import sys
import argparse
from pathlib import Path

import yaml
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)

from crawler import collect_code, find_extensions

from llm import (
    check_context_window,
    generate_docs,
    models,
)

# Initialize rich console for styled output
console = Console()


def load_config(path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def prompt_user() -> dict:
    """Interactively prompt the user for settings if no config file is provided."""
    code_path = questionary.path(
        "Enter the path to the code directory or file:", only_directories=False
    ).ask()

    save_same = questionary.confirm(
        "Save documentation in the same directory as source?", default=True
    ).ask()
    if save_same:
        output_dir = (
            code_path if os.path.isdir(code_path) else str(Path(code_path).parent)
        )
    else:
        output_dir = questionary.path(
            "Enter the output directory for the documentation:", only_directories=True
        ).ask()

    blacklist = (
        questionary.checkbox(
            "Select any of the found extensions you'd like to skip entirely:",
            choices=find_extensions(code_path),
        ).ask()
        or []
    )

    doc_options = [
        "Readme",
        "API documentation",
        "Quickstart guide",
        "Tutorial",
        "User guide",
        "Reference",
    ]
    doc_types = questionary.checkbox(
        "Select the types of documentation to generate (use space to select, enter to confirm):",
        choices=doc_options,
    ).ask()

    custom_instructions = (
        questionary.text(
            "Enter any custom instructions for the language model (optional):"
        ).ask()
        or ""
    )

    model_choice = questionary.select(
        "Select the model to use:",
        choices=list(models.keys()),
        default=list(models.keys())[0],
    ).ask()

    save_settings = questionary.confirm(
        "Save current settings to config.yaml?", default=True
    ).ask()
    settings = {
        "code_path": code_path,
        "output_dir": output_dir,
        "blacklist": blacklist,
        "doc_types": doc_types,
        "custom_instructions": custom_instructions,
        "model": model_choice,
    }

    if save_settings:
        with open("config.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(settings, f)
        console.print(":bookmark_tabs: Settings saved to config.yaml")

    return settings


def write_to_file(filename: str, content: str):
    """Write generated content to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]POSTDOC[/bold cyan]: The [bold magenta]🧙 wizard[/bold magenta] for effortlessly conjuring [bold spring_green3]high-quality[/bold spring_green3] documentation!",
            title="🪄 [bold cyan]POSTDOC[/bold cyan] 🪄",
            border_style="bright_cyan",
            padding=(1, 4),
        )
    )

    parser = argparse.ArgumentParser(
        description="POSTDOC: Generate project documentation using OpenAI"
    )
    parser.add_argument(
        "-c", "--config", help="Path to a YAML config file with settings", type=str
    )
    args = parser.parse_args()

    cfg = load_config(args.config) if args.config else prompt_user()
    code_path = cfg.get("code_path")
    output_dir = cfg.get("output_dir")
    blacklist = cfg.get("blacklist")
    doc_types = cfg.get("doc_types") or []
    model = cfg.get("model")
    custom_instruct = cfg.get("custom_instructions") or ""

    if custom_instruct is None:
        custom_instruct = ""

    if not doc_types:
        console.print(
            "Error: No documentation types selected. Goodbye!", style="bold red"
        )
        sys.exit(1)

    console.print(f"Collecting code from [bold]{code_path}[/bold]")
    code = collect_code(code_path, blacklist)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        token_count, context_window, fallback = check_context_window(
            model, custom_instruct, code
        )
    except KeyError:
        console.print(f"[bold red]Error:[/] Unknown model {model!r}")
        return

    if fallback:
        console.print(
            f"[yellow]Tokenizer for {model} not found; "
            f"falling back to {fallback}[/yellow]"
        )

    console.print(f"[blue]Total input tokens:[/blue] {token_count}")

    if token_count > context_window:
        console.print(
            Panel(
                f"❌ Your input is {token_count} tokens, "
                f"exceeding the {context_window}-token limit for {model}.",
                title="Token Limit Exceeded",
                style="bold red",
            ),
            justify="center",
        )
        sys.exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        check_context_window(model, custom_instruct, code)

        for doc_type in doc_types:
            instruct = (
                "If the documentation already exists. Update, proofread, and tweak it, making only minimal, safe changes. "
                "Preserve all critical information or replace with equivalent, updated information. "
                "IMPORTANT: do NOT introduce major rewrites or alter content unnecessarily."
                f"{custom_instruct}"
            )

            prompt = f"Generate or update {doc_type} for {code}"

            task = progress.add_task(f"Generating {doc_type}...", total=None)
            result = generate_docs(model, instruct, prompt)
            out_file = Path(output_dir) / f"{doc_type.lower().replace(' ', '_')}.md"
            write_to_file(str(out_file), result)
            progress.update(task, completed=1)

    console.print(":white_check_mark: Documents generated, goodbye!")


if __name__ == "__main__":
    main()
