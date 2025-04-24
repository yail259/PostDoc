#!/usr/bin/env python3
"""
POSTDOC CLI Tool

This script generates documentation for a codebase using a variety of LLM providers.
It delegates all actual LLM calls to the separate `llm.py` module via a unified `generate_docs` function.
Supported providers: OpenAI, AzureOpenAI, Anthropic, Gemini, Ollama.
"""

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
from llm import build_instruction, check_context_window, generate_docs, models

console = Console()


def load_config(path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def prompt_user() -> dict:
    """Interactively prompt the user for settings if no config file is provided."""
    code_path = questionary.path(
        "Enter the path to the code directory:", only_directories=True
    ).ask()

    save_same = questionary.confirm(
        "Save documentation in the same directory as source?", default=True
    ).ask()
    output_dir = (
        str(Path(code_path))
        if save_same
        else questionary.path(
            "Enter the output directory:", only_directories=True
        ).ask()
    )

    blacklist = (
        questionary.checkbox(
            "Skip files with these extensions:",
            choices=find_extensions(code_path),
        ).ask()
        or []
    )

    doc_types = (
        questionary.checkbox(
            "Select documentation types to generate:",
            choices=[
                "Readme",
                "API documentation",
                "Quickstart guide",
                "Tutorial",
                "User guide",
                "Reference",
            ],
        ).ask()
        or []
    )

    custom_instructions = (
        questionary.text("Enter any custom instructions (optional):").ask() or ""
    )

    model_choice = questionary.select(
        "Select the LLM model to use:",
        choices=list(models.keys()),
        default=list(models.keys())[0],
    ).ask()

    provider_choice = questionary.select(
        "Select your LLM provider:",
        choices=["OpenAI", "AzureOpenAI", "Anthropic", "Gemini", "Ollama"],
        default="OpenAI",
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
        "provider": provider_choice,
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
            "[bold cyan]POSTDOC[/bold cyan]: The 🧙 wizard for conjuring high-quality docs!",
            title="🪄 POSTDOC 🪄",
            border_style="bright_cyan",
            padding=(1, 4),
        )
    )

    parser = argparse.ArgumentParser(description="POSTDOC: Generate project docs")
    parser.add_argument("-c", "--config", help="YAML config file", type=str)

    args = parser.parse_args()

    cfg = load_config(args.config) if args.config else prompt_user()

    code_path = cfg["code_path"]
    output_dir = cfg["output_dir"]
    blacklist = cfg.get("blacklist", [])
    doc_types = cfg.get("doc_types", [])
    model = cfg.get("model")
    provider = cfg.get("provider")
    custom_instruct = cfg.get("custom_instructions", "") or ""

    if not doc_types:
        console.print("No documentation types selected, exiting.", style="bold red")
        sys.exit(1)

    console.print(f"Collecting code from [bold]{code_path}[/bold]")
    code = collect_code(code_path, blacklist)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        token_count, ctx_win, fallback = check_context_window(
            model, custom_instruct, code
        )
    except KeyError:
        console.print(f"[bold red]Error:[/] Unknown model {model!r}")
        sys.exit(1)

    if fallback:
        console.print(f"[yellow]Falling back to tokenizer {fallback}[/yellow]")
    console.print(f"[blue]Tokens in input:[/] {token_count}")

    if token_count > ctx_win:
        console.print(
            Panel(
                f"❌ {token_count} tokens > {ctx_win} token limit for {model}",
                title="Context Window Exceeded",
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
    ) as prog:
        for doc_type in doc_types:
            instruct = build_instruction(
                doc_type, custom_instruct, output_dir, code_path
            )

            prompt = f"Generate or update {doc_type} for:\n{code}"

            task = prog.add_task(f"Generating {doc_type}…", total=1)

            # Delegate actual LLM call to llm.py
            result = generate_docs(model, instruct, prompt, provider=provider)

            out = Path(output_dir) / f"{doc_type.lower().replace(' ', '_')}.md"
            write_to_file(str(out), result)
            prog.update(task, completed=1)

    console.print(":white_check_mark: Documents generated! Goodbye.")


if __name__ == "__main__":
    main()
