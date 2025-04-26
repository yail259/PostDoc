#!/usr/bin/env python3
"""
runesmith CLI Tool (Upgraded)

Multi-stage document generation:
- Per-chunk LLM documentation
- Merge or Smooth final docs based on type
- Supports large codebases
"""

import sys

import shutil
from pathlib import Path
import yaml
import typer
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
from collections import defaultdict

from runesmith.crawler import collect_code_chunks, find_extensions
from runesmith.llm import (
    build_instruction,
    check_context_window,
    count_tokens,
    generate_docs,
    PROVIDER_MODELS,
    get_context_window,
    get_ollama_models,
)

console = Console()
app = typer.Typer(
    help="🧙 runesmith: Conjure professional documentation automatically!"
)


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_to_file(filename: str, content: str):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def prompt_user() -> dict:
    provider_choice = questionary.select(
        "Select your LLM provider:",
        choices=list(PROVIDER_MODELS.keys()) + ["Ollama"],
        default="OpenAI",
    ).ask()

    if provider_choice == "Ollama":
        model_names = get_ollama_models()
        model_choice = questionary.select(
            "Select an Ollama model:",
            choices=model_names,
            default=model_names[0] if model_names else None,
        ).ask()
    else:
        model_dict = PROVIDER_MODELS.get(provider_choice, {})
        model_names = list(model_dict.keys())
        model_choice = questionary.select(
            f"Select the LLM model to use from {provider_choice}:",
            choices=model_names,
            default=model_names[0] if model_names else None,
        ).ask()

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

    save_settings = questionary.confirm(
        "Save current settings to config.yaml?", default=True
    ).ask()

    settings = {
        "provider": provider_choice,
        "model": model_choice,
        "code_path": code_path,
        "output_dir": output_dir,
        "blacklist": blacklist,
        "doc_types": doc_types,
        "custom_instructions": custom_instructions,
    }

    if save_settings:
        with open("config.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(settings, f)
        console.print(":bookmark_tabs: Settings saved to config.yaml")

    return settings


def generate_from_config(cfg: dict):
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

    console.print(
        Panel.fit(
            "[bold cyan]runesmith[/bold cyan]: The 🧙 wizard for conjuring high-quality docs!",
            title="🪄 runesmith 🪄",
            border_style="bright_cyan",
            padding=(1, 4),
        )
    )

    console.print(f"Collecting code from [bold]{code_path}[/bold]")
    chunks = []
    for chunk, warnings in collect_code_chunks(code_path, blacklist):
        for warning in warnings:
            console.print(f"[yellow]{warning}[/yellow]")
        chunks.append(chunk)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    chunk_docs = []

    doc_folder = Path(output_dir) / "cache_docs"
    doc_folder.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as prog:
        task = prog.add_task("Summarising individual files…", total=len(chunks))

        for chunk in chunks:
            instruct = (
                "You are a professional technical writer. Summarise and list the technical"
                "elements of this file. The reader is also an expert so priorities preserving details whilst"
                "condensing information."
                "Multiple of such summaries of individual files will be combined into "
                "{' '.join(doc_types)} documentation files.\n"
            )
            result = generate_docs(
                model,
                instruct,
                f"\n# File: {chunk['path']}\n{chunk['content']}",
                provider=provider,
            )

            out_path = (
                doc_folder / f"{chunk['path'].replace('/', '_').replace('.', '_')}.md"
            )
            write_to_file(out_path, result)

            chunk_docs.append(result)
            prog.advance(task)

    for doc_type in doc_types:
        instruct_template = build_instruction(
            doc_type, custom_instruct, output_dir, code_path
        )

        # Post-processing phase
        console.print(f":sparkles: Smoothing {doc_type} output with LLM...")
        combined_draft = "\n\n".join(chunk_docs)
        final_prompt = f"You are a professional technical writer. Merge and organize \
            the following {doc_type} drafts into a coherent document with clear structure, \
            no duplication, and polished transitions.\n\n{combined_draft}"
        smoothed_result = generate_docs(
            model,
            instruct_template,
            final_prompt,
            provider=provider,
        )
        final_out = Path(output_dir) / f"{doc_type.lower().replace(' ', '_')}.md"
        write_to_file(final_out, smoothed_result)

    console.print(":white_check_mark: All documents generated successfully! Goodbye.")
    # shutil.rmtree(doc_folder)


@app.command()
def generate(
    config: Path = typer.Option(
        None, "--config", "-c", help="Path to YAML config file"
    ),
):
    if config:
        cfg = load_config(str(config))
    else:
        cfg = prompt_user()

    generate_from_config(cfg)


if __name__ == "__main__":
    app()
