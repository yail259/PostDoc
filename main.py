#!/usr/bin/env python3
"""
POSTDOC CLI Tool

This script generates documentation for a codebase or single file using OpenAI's API.
It can load settings from a YAML config file or interactively prompt the user.
"""

import os
import sys
import argparse
from pathlib import Path

import yaml
from openai import OpenAI
import tiktoken
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

from dotenv import load_dotenv

# Initialize rich console for styled output
console = Console()

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

# Supported models and their context window sizes
models = {"gpt-4.1": {"context_window": 1047576}}


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
        "doc_types": doc_types,
        "custom_instructions": custom_instructions,
        "model": model_choice,
    }

    if save_settings:
        with open("config.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(settings, f)
        console.print(":bookmark_tabs: Settings saved to config.yaml")

    return settings


def check_context_window(model: str, instruct: str, prompt: str):
    """Count tokens and ensure they fit within the model's context window."""
    context_window = models[model]["context_window"]

    try:
        encoding = tiktoken.encoding_for_model(model)
    except Exception:
        fallback = "o200k_base"
        console.print(
            f"[yellow]Tokenizer for {model} not found; falling back to {fallback}[/yellow]"
        )
        encoding = tiktoken.get_encoding(fallback)

    full_prompt = instruct + "\n" + prompt
    # Allow special tokens in encoding to avoid errors
    token_count = len(encoding.encode(full_prompt, disallowed_special=()))
    console.print(f"[blue]Total input tokens:[/blue] {token_count}")

    if token_count > context_window:
        console.print(
            Panel(
                f"❌ Your input is {token_count} tokens, exceeding the {context_window}-token limit for {model}.",
                title="Token Limit Exceeded",
                style="bold red",
            ),
            justify="center",
        )
        sys.exit(1)


def collect_code(path: str, file_extensions=None) -> str:
    """Collect code content from a directory or single file into a string."""
    if file_extensions is None:
        file_extensions = [".py", ".js", ".ts", ".java", ".go", ".c", ".cpp", ".cs"]

    code_str = ""
    p = Path(path)
    if p.is_file():
        if any(p.name.endswith(ext) for ext in file_extensions):
            try:
                code_str = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                console.log(f"Warning: Could not read file {p}")
        else:
            console.print(
                f"Warning: File {p} does not match extensions; skipping.",
                style="yellow",
            )
    elif p.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    filepath = os.path.join(root, file)
                    try:
                        with open(
                            filepath, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            code_str += f"\n\n# File: {filepath}\n" + f.read()
                    except Exception:
                        console.log(f"Warning: Could not read file {filepath}")
    else:
        console.print(f"Error: Path {path} not found.", style="bold red")
        sys.exit(1)
    return code_str


def generate_docs(model: str, instruct: str, prompt: str) -> str:
    """Use OpenAI's API to generate documentation of the specified type."""
    response = client.responses.create(
        model=model,
        instructions=instruct,
        input=prompt,
    )
    return response.output_text


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

    try:
        cfg = load_config(args.config) if args.config else prompt_user()
        code_path = cfg.get("code_dir")
        output_dir = cfg.get("output_dir")
        doc_types = cfg.get("doc_types", [])
        model = cfg.get("model")
        custom_instruct = cfg.get("custom_instructions", "")

        if not doc_types:
            console.print(
                "Error: No documentation types selected. Goodbye!", style="bold red"
            )
            sys.exit(1)

        console.print(f"Collecting code from [bold]{code_path}[/bold]...")
        code = collect_code(code_path)
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            transient=True,
        ) as progress:
            for doc_type in doc_types:
                instruct = f"You are a helpful assistant that writes high-quality {doc_type} for developers. {custom_instruct}"
                prompt = (
                    f"Generate a complete {doc_type} for the following codebase. {code}"
                )

                check_context_window(model, instruct, prompt)

                task = progress.add_task(f"Generating {doc_type}...", total=None)
                result = generate_docs(model, instruct, prompt)
                out_file = Path(output_dir) / f"{doc_type.lower().replace(' ', '_')}.md"
                write_to_file(str(out_file), result)
                progress.update(task, completed=1)

        console.print(":white_check_mark: Documents generated, goodbye!")

    except Exception as e:
        console.print(f":x: Error: {e}, goodbye!", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
