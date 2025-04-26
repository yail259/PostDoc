# Runesmith API & Technical Documentation

---

## Table of Contents

1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Usage](#usage)
    - [Interactive Mode](#interactive-mode)
    - [Config-Driven Mode](#config-driven-mode)
    - [Configuration Options](#configuration-options)
6. [CLI Reference](#cli-reference)
7. [LLM Provider Integration](#llm-provider-integration)
8. [Internal Workflow](#internal-workflow)
    - [Codebase Crawling](#codebase-crawling)
    - [Token Counting & Context Management](#token-counting--context-management)
    - [Documentation Generation](#documentation-generation)
9. [Dependency Management](#dependency-management)
10. [Project Structure](#project-structure)
11. [Extending Runesmith](#extending-runesmith)
12. [.gitignore Policy](#gitignore-policy)
13. [Versioning & Python Version](#versioning--python-version)
14. [License](#license)
15. [Acknowledgements](#acknowledgements)
16. [Planned Enhancements](#planned-enhancements)
17. [Contribution Guidelines](#contribution-guidelines)

---

## Overview

**Runesmith** is a Python-based CLI tool for generating, updating, and managing code documentation using large language models (LLMs) such as OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama. It is designed to automate and streamline the creation of high-quality documentation for codebases, supporting both interactive and configuration-driven workflows.

Runesmith also provides infrastructure-as-code (IaC) blueprint management capabilities, focusing on modular, reusable, and composable infrastructure definitions for cloud-agnostic deployments.

---

## Core Features

- **Automatic Documentation Generation**: Generate or update documentation for entire codebases or individual files using LLMs.
- **Multi-Provider LLM Support**: Integrates with OpenAI, Azure OpenAI, Anthropic, Gemini, and local Ollama models.
- **Context Awareness**: Honors `.gitignore`, existing documentation, and makes minimal, safe changes.
- **Interactive Wizard & Config-Driven Operation**: Choose between a guided CLI wizard or YAML configuration files.
- **Customizability**: Select documentation types, blacklist file extensions, and add custom LLM instructions.
- **Token Safety**: Warns if the codebase exceeds the model's context window.
- **Per-Chunk Summarization**: Scales to large codebases by summarizing code in manageable chunks.
- **Smoothing & Merging**: Optionally merges and polishes chunk summaries for coherent, high-quality documentation.
- **IaC Blueprint Management**: Author, compose, validate, and deploy infrastructure blueprints with versioning and state management.

---

## Architecture

- **CLI Tool**: Written in Python, using [Typer](https://typer.tiangolo.com/) for the command-line interface.
- **Modular Design**: Plugin-based architecture for extensibility (e.g., custom providers, workflows).
- **Declarative Approach**: Infrastructure definitions via YAML/JSON.
- **Provider Integration**: Interacts with cloud providers via SDKs or CLIs.
- **State & Version Management**: Tracks deployed resources and supports version control for blueprints and deployments.

---

## Installation & Setup

### Prerequisites

- **Python**: Version 3.10 (specified in `.python-version` for tools like pyenv).
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**: For dependency management and virtual environments.

### Steps

1. **Clone the Repository**
    ```bash
    git clone <repo-url>
    cd runesmith
    ```

2. **Install Dependencies**
    ```bash
    uv sync
    ```

3. **Activate the Virtual Environment**
    ```bash
    source .venv/bin/activate
    ```

4. **Set Up Environment Variables**
    - Create a `.env` file in the project root or export variables directly (see [LLM Provider Integration](#llm-provider-integration)).

---

## Usage

### Interactive Mode

Launch the guided wizard to configure and generate documentation:

```bash
runesmith generate
```

### Config-Driven Mode

Use a YAML configuration file for repeatable, automated runs:

```bash
runesmith generate --config config.yaml
```

#### Example `config.yaml`

```yaml
provider: openai
model: gpt-4o
code_path: ./src
output_dir: ./docs
blacklist:
  - .pyc
  - .pyo
doc_types:
  - Readme
  - API docs
  - Quickstart
custom_instruct: |
  Please focus on clarity and conciseness.
```

#### Configuration Options

- **provider**: LLM provider (`openai`, `azure`, `anthropic`, `gemini`, `ollama`)
- **model**: Model name (e.g., `gpt-4o`, `claude-3.5-haiku`)
- **code_path**: Path to codebase to document
- **output_dir**: Directory for generated documentation
- **blacklist**: List of file extensions to ignore
- **doc_types**: Types of documentation to generate (e.g., `Readme`, `API docs`, `Quickstart`, `Tutorial`, `User guide`, `Reference`)
- **custom_instruct**: Additional instructions for the LLM

---

## CLI Reference

The CLI is implemented using [Typer](https://typer.tiangolo.com/). The main entry point is:

```bash
runesmith generate [--config config.yaml]
```

- **Interactive prompts**: If no config is provided, the CLI will guide you through provider/model selection, code/output directories, blacklist, doc types, and custom instructions.
- **Config file**: If `--config` is specified, settings are loaded from the YAML file.

**Workflow:**

1. Collect code chunks (respecting `.gitignore` and blacklist).
2. For each chunk, generate a technical summary using the selected LLM.
3. Write per-chunk summaries to a temporary folder.
4. For each documentation type:
    - If smoothing/merging is required (e.g., API docs), merge chunk summaries using the LLM.
    - Otherwise, mark as complete.
5. Clean up temporary files.

---

## LLM Provider Integration

### Supported Providers & Models

| Provider      | Example Models                        | Notes                        |
|---------------|--------------------------------------|------------------------------|
| OpenAI        | gpt-4o, gpt-4-turbo, gpt-4.5         | Default, tested              |
| Azure OpenAI  | gpt-4o, gpt-4-turbo                  | Requires Azure credentials   |
| Anthropic     | claude-3.5-haiku, claude-3-opus      |                              |
| Gemini        | gemini-1.5-pro, gemini-2.5-pro       |                              |
| Ollama        | Any local model                      | No API key required, tested  |

### Environment Variables

| Provider      | Required Variables                                                                 |
|---------------|------------------------------------------------------------------------------------|
| OpenAI        | `OPENAI_API_KEY`                                                                   |
| Azure OpenAI  | `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`            |
| Anthropic     | `ANTHROPIC_API_KEY`                                                                |
| Gemini        | `GEMINI_API_KEY`                                                                   |
| Ollama        | None                                                                               |

- All providers support loading variables from a `.env` file in the project root.

---

## Internal Workflow

### Codebase Crawling

- **Module**: `runesmith.crawler`
- **Functions**:
    - `collect_code_chunks(dir_path, blacklist)`: Recursively yields code chunks, skipping files per `.gitignore` and blacklist.
    - `find_extensions(dir_path)`: Lists unique file extensions in the codebase.

### Token Counting & Context Management

- **Module**: `runesmith.llm`
- **Functions**:
    - `count_tokens(text, model)`: Uses `tiktoken` to count tokens for the selected model.
    - `get_context_window(provider, model)`: Returns the model's context window size.
    - Warns if the codebase exceeds the model's context window.

### Documentation Generation

- **Per-Chunk Summarization**: Each code chunk is summarized by the LLM.
- **Smoothing/Merging**: For certain doc types (e.g., API docs), chunk summaries are merged and polished by the LLM.
- **Minimal Updates**: Existing documentation is updated minimally and safely.

---

## Dependency Management

- **Dependency Locking**: Uses `uv.lock` for deterministic, reproducible installs.
- **Dependency Graph**: All direct and transitive dependencies are pinned with SHA256 hashes for security.
- **Editable Install**: The main project is installed in editable mode for development.

### Main Packages

| Package           | Version   | Role/Functionality                |
|-------------------|-----------|-----------------------------------|
| runesmith         | 0.1.0     | Main project                      |
| ollama            | 0.4.8     | LLM API client                    |
| openai            | 1.76.0    | OpenAI API client                 |
| tiktoken          | 0.9.0     | Tokenizer for LLMs                |
| typer             | 0.15.2    | CLI framework                     |
| questionary       | 2.1.0     | Interactive CLI prompts           |
| rich              | 14.0.0    | Terminal formatting               |
| pydantic          | 2.11.3    | Data validation                   |
| httpx             | 0.28.1    | HTTP client                       |
| requests          | 2.32.3    | HTTP client                       |
| python-dotenv     | 1.1.0     | .env file loader                  |
| pyyaml            | 6.0.2     | YAML parsing                      |
| pathspec          | 0.12.1    | Path pattern matching             |

---

## Project Structure

```
runesmith/
├── src/
│   └── runesmith/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── crawler.py
│       └── llm.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── README.md
└── LICENSE
```

- **src/runesmith/__init__.py**: Package initializer.
- **src/runesmith/cli.py**: CLI implementation.
- **src/runesmith/crawler.py**: Codebase crawling and file filtering.
- **src/runesmith/llm.py**: LLM provider integration and utilities.
- **src/runesmith/__main__.py**: CLI entry point.
- **pyproject.toml**: Project metadata, dependencies, and build system.
- **uv.lock**: Locked dependency versions and hashes.
- **.python-version**: Specifies Python 3.10 for development.
- **.gitignore**: Excludes generated, environment-specific, and project-specific files.

---

## Extending Runesmith

- **Custom Providers**: Add via the plugin interface.
- **Hooks**: Pre/post-deployment actions for IaC workflows.
- **Blueprints**: Author in `/blueprints` directory using YAML/JSON.
- **Examples & Docs**: See `/examples` and `/docs` for usage scenarios and API/plugin documentation.

---

## .gitignore Policy

The `.gitignore` file is configured to:

- Ignore Python bytecode and cache directories: `__pycache__/`, `*.pyc`, `*.pyo`
- Exclude build artifacts and distribution directories: `build/`, `dist/`, `wheels/`, `*.egg-info`
- Omit virtual environment directories and environment files: `.venv`, `*.env`
- Ignore files/directories matching `batch*`, `config*`
- Exclude the `web/` directory and `test.py` file

This prevents versioning of generated, environment-specific, and certain project-specific files and directories.

---

## Versioning & Python Version

- **Project Version**: 0.1.0 (see `pyproject.toml`)
- **Python Version**: 3.10 (enforced via `.python-version`)

---

## License

**MIT License**  
Copyright (c) 2025 yail259

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**Disclaimer**:  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Acknowledgements

- [uv](https://github.com/astral-sh/uv) for dependency management
- [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Questionary](https://github.com/tmbo/questionary), and other open-source libraries

---

## Planned Enhancements

- Add generated docs to LLM context window for improved updates
- Retrieval-Augmented Generation (RAG) for large codebases
- Package as a standalone binary
- Multilanguage support
- Iterative prompting/looping for refinement

---

## Contribution Guidelines

- Open-source under the MIT License.
- Contribution guidelines are provided in the repository.
- Please see the `CONTRIBUTING.md` file for details on submitting issues and pull requests.

---

*This documentation is self-generated and updated by Runesmith.*