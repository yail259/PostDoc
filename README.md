# Runesmith 🧙

**Runesmith** is a Python CLI tool for automated, high-quality codebase documentation generation and management using Large Language Models (LLMs) such as OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama. It supports both interactive and configuration-driven workflows, and is designed for extensibility, reproducibility, and safe, minimal updates to existing documentation.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Quickstart](#quickstart)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Supported Providers & Models](#supported-providers--models)
8. [Environment Variables](#environment-variables)
9. [Internal Workflow](#internal-workflow)
10. [Architecture & Project Structure](#architecture--project-structure)
11. [Dependency Management](#dependency-management)
12. [Extensibility](#extensibility)
13. [Planned Enhancements](#planned-enhancements)
14. [Contributing](#contributing)
15. [License](#license)
16. [Changelog](#changelog)
17. [Acknowledgements](#acknowledgements)

---

## Overview

Runesmith automates the generation and updating of documentation for codebases, including READMEs, API docs, tutorials, quickstarts, and more. It leverages LLMs to summarize, synthesize, and polish documentation, while respecting your codebase’s structure, `.gitignore`, and existing documentation. Runesmith is also extensible for infrastructure-as-code (IaC) blueprints and prompt management.

---

## Key Features

- **Automatic Documentation**: Generate or update documentation for your codebase with a single command.
- **Multi-Provider LLM Support**: OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local).
- **Context Awareness**: Honors `.gitignore`, blacklists, and existing docs; makes only minimal, safe changes.
- **Interactive & Config Modes**: Use an interactive wizard or a YAML config file.
- **Customization**: Select doc types, blacklist file extensions, and add custom LLM instructions.
- **Token Safety**: Warns if your codebase exceeds the LLM’s context window.
- **IaC Blueprints**: Modular, composable infrastructure blueprints for cloud-agnostic deployments (YAML/JSON).
- **Extensibility**: Plugin-based architecture for providers and workflows.
- **Prompt Management**: YAML-based prompt definitions, chaining, and versioning.
- **Testing & Validation**: Tools for prompt and documentation validation.

---

## Installation

### Option 1: Install via PyPI

```bash
pip install runesmith
```

### Option 2: Install from Source (Recommended for Development)

1. **Install [uv](https://docs.astral.sh/uv/getting-started/installation/):**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the Repository and Install Dependencies:**

   ```bash
   git clone https://github.com/yail259/runesmith.git
   cd runesmith
   uv sync
   ```

   This creates a `.venv` and installs all dependencies as specified in `pyproject.toml` and `uv.lock`.

3. **Activate the Virtual Environment:**

   ```bash
   source .venv/bin/activate
   ```

---

## Quickstart

1. **Generate Documentation (Interactive Wizard):**

   ```bash
   runesmith generate
   ```

   - You will be guided through provider/model selection, code path, output directory, doc types, and custom instructions.
   - Optionally, save your settings to `config.yaml` for future runs.

2. **Generate Documentation from Config:**

   ```bash
   runesmith generate --config config.yaml
   ```

---

## Usage

### CLI Commands

- **Interactive Mode:**

  ```bash
  runesmith generate
  ```

- **Config-Driven Mode:**

  ```bash
  runesmith generate --config config.yaml
  ```

### Example `config.yaml`

```yaml
provider: OpenAI
model: gpt-4o
code_path: ./src
output_dir: ./docs
blacklist: [".env", ".pyc"]
doc_types:
  - Readme
  - API documentation
  - Quickstart guide
custom_instructions: |
  Please focus on developer experience and include usage examples.
```

---

## Configuration

- **Interactive Wizard**: Prompts for all options (provider, model, code path, output dir, blacklist, doc types, custom instructions).
- **YAML Config**: All options can be specified in a YAML file for reproducible runs.
- **Environment Variables**: API keys and secrets can be set via environment variables or a `.env` file.

---

## Supported Providers & Models

- **OpenAI**: gpt-4o, gpt-4-turbo, gpt-4.5, etc.
- **Azure OpenAI**: gpt-4o, gpt-4-turbo, etc.
- **Anthropic**: claude-3.5-haiku, claude-3-opus, etc.
- **Gemini**: gemini-1.5-pro, gemini-2.5-pro, etc.
- **Ollama**: Any local model available via Ollama.

> **Note:** Only OpenAI and Ollama are tested by default. For other providers, ensure you have the correct API keys and environment variables set.

---

## Environment Variables

Set the following environment variables as needed for your provider (can be placed in a `.env` file):

- **OpenAI**: `OPENAI_API_KEY`
- **Azure OpenAI**: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Gemini**: `GEMINI_API_KEY`
- **Ollama**: (runs locally, no key needed)

---

## Internal Workflow

1. **Crawling**: Scans your codebase, respecting `.gitignore` and skipping blacklisted extensions.
2. **Token Counting**: Warns if your codebase exceeds the model's context window.
3. **Per-Chunk Summarization**: Each file is summarized via the selected LLM.
4. **Merging & Smoothing**: Summaries are merged and polished into final documentation per doc type.
5. **Safe Updates**: If documentation already exists, Runesmith will only make minimal, safe changes.
6. **Output**: Final documentation is written to the specified output directory.

---

## Architecture & Project Structure

- **CLI**: Built with [Typer](https://typer.tiangolo.com/).
- **Modular/Plugin Design**: Extensible for providers and workflows.
- **Declarative IaC**: YAML/JSON blueprints for infrastructure.
- **Provider SDK/CLI Integration**: For cloud operations.
- **State/Version Tracking**: For blueprints and deployments.

**Project Layout:**

```
src/runesmith/
  __init__.py
  __main__.py
  cli.py
  crawler.py
  llm.py
pyproject.toml
uv.lock
.python-version
.gitignore
README.md
LICENSE
```

---

## Dependency Management

- **Lockfile**: `uv.lock` with SHA256 hashes for reproducible installs.
- **Editable Install**: For development.
- **Key Packages**: `ollama`, `openai`, `tiktoken`, `typer`, `questionary`, `rich`, `pydantic`, `httpx`, `requests`, `python-dotenv`, `pyyaml`, `pathspec`.
- **Python Version**: 3.10 (enforced via `.python-version`).

---

## Extensibility

- **Custom Providers**: Add new LLM providers via plugin interface.
- **Hooks**: Pre/post-deployment for IaC.
- **Blueprints**: Authored in `/blueprints` (YAML/JSON).
- **Prompt Management**: YAML-based prompt definitions, chaining, and versioning.
- **Testing & Validation**: Built-in tools for prompt and documentation validation.

---

## Planned Enhancements

- Add generated docs to LLM context for updates.
- Retrieval-Augmented Generation (RAG) for context window issues.
- Standalone binary packaging.
- Multilanguage support.
- Iterative prompting/looping.

---

## Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/yail259/runesmith). See `CONTRIBUTING.md` for guidelines.

---

## License

MIT License © 2025 yail259

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Changelog

### 0.1.0 (2025-06)
- Initial public release.
- Multi-provider LLM support (OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama).
- Interactive and config-driven documentation generation.
- Context-aware codebase crawling with `.gitignore` and blacklist support.
- Per-chunk summarization and final doc synthesis.
- Minimal, safe updates to existing documentation.
- IaC blueprint support (YAML/JSON).
- Plugin-based extensibility for providers and workflows.
- Token counting and context window warnings.
- PyPI package published (`pip install runesmith`).

---

## Acknowledgements

- [uv](https://astral.sh/uv/) for fast Python dependency management.
- [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Questionary](https://github.com/tmbo/questionary), and all other open-source dependencies.

---

## .gitignore Policy

- Excludes Python bytecode, build/dist artifacts, venvs, env files, batch/config files, web directory, test scripts, and cache files.
- Purpose: Prevents version control of generated, environment-specific, and temporary files to maintain repository cleanliness.

---

**Happy documenting! 🧙‍♂️**

---

> _This README was generated and updated by runesmith itself!_