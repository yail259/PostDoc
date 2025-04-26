# Runesmith: Automated Code Documentation with LLMs

---

## Overview

**Runesmith** is a Python CLI tool for automated, high-quality codebase documentation generation and management using Large Language Models (LLMs) such as OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local). It supports both interactive wizard-driven and YAML configuration-driven workflows, and is extensible for infrastructure-as-code (IaC) blueprint authoring and deployment.

---

## Table of Contents

1. [Core Functionality](#core-functionality)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Usage](#usage)
6. [CLI Reference](#cli-reference)
7. [LLM Provider Integration](#llm-provider-integration)
8. [Internal Workflow](#internal-workflow)
9. [Dependency Management](#dependency-management)
10. [Project Structure](#project-structure)
11. [Extensibility](#extensibility)
12. [.gitignore Policy](#gitignore-policy)
13. [Versioning](#versioning)
14. [License](#license)
15. [Changelog](#changelog)
16. [Planned Enhancements](#planned-enhancements)
17. [Contribution](#contribution)

---

## Core Functionality

- **Purpose**:  
  Runesmith automates the generation and updating of documentation for codebases or files using LLM APIs. It can produce READMEs, API docs, tutorials, quickstarts, and more, with minimal and safe updates to existing documentation.
- **Modes**:  
  - **Interactive CLI Wizard**: Guided setup for provider/model selection, codebase path, output directory, blacklist, doc types, and custom instructions.
  - **YAML Config-Driven**: All options can be specified in a `config.yaml` file for reproducible, automated runs.
- **IaC Support**:  
  Modular, composable infrastructure blueprints for cloud-agnostic deployments, with authoring, validation, and deployment capabilities.

---

## Key Features

- **LLM Integration**:  
  Supports multiple providers and models, custom instructions, and context window/token management.
- **Documentation Generation**:  
  Per-chunk summarization, smoothing/merging, minimal/safe updates, and doc type selection.
- **Codebase Awareness**:  
  Honors `.gitignore`, extension blacklists, and existing documentation.
- **IaC Blueprints**:  
  Author, compose, validate, and deploy blueprints with version/state management.
- **Extensibility**:  
  Plugin-based architecture for providers and workflows.

---

## Architecture

- **CLI**:  
  Built with [Typer](https://typer.tiangolo.com/) for robust command-line interfaces.
- **Modular/Plugin Design**:  
  Extensible for new providers and workflows.
- **Declarative IaC**:  
  YAML/JSON blueprints for infrastructure definitions.
- **Provider SDK/CLI Integration**:  
  For cloud operations and deployments.
- **State/Version Tracking**:  
  For blueprints and deployments.

---

## Installation & Setup

### Requirements

- **Python 3.10** (enforced via `.python-version`)

### Install via PyPI

```bash
pip install runesmith
```

### Development Setup

- **Dependency Management**:  
  Uses [uv](https://astral.sh/uv/) and `uv.lock` for reproducible installs.
- **Clone and Install**:
  ```bash
  git clone https://github.com/yourorg/runesmith.git
  cd runesmith
  uv sync
  source .venv/bin/activate
  ```

### Environment Variables

- Store LLM credentials in a `.env` file or export them directly:
  - `OPENAI_API_KEY`
  - `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
  - `ANTHROPIC_API_KEY`
  - `GEMINI_API_KEY`
  - Ollama requires no API key (local only)

---

## Usage

### Interactive Mode

```bash
runesmith generate
```
- Guided prompts for all options.

### Config-Driven Mode

```bash
runesmith generate --config config.yaml
```
- Example `config.yaml` options:
  - Provider/model selection
  - Code and output paths
  - Blacklist extensions
  - Doc types list
  - Custom LLM instructions

---

## CLI Reference

- **Entry Point**:  
  `runesmith generate [--config config.yaml]`
- **Workflow**:
  1. Crawl codebase (respects `.gitignore` and blacklist)
  2. Summarize code chunks via LLM
  3. Write summaries to a temporary folder
  4. Merge/polish as needed per doc type
  5. Clean up

---

## LLM Provider Integration

- **Supported Providers**:
  - **OpenAI**: gpt-4o, gpt-4-turbo, gpt-4.5, etc.
  - **Azure OpenAI**: gpt-4o, gpt-4-turbo, etc.
  - **Anthropic**: claude-3.5-haiku, claude-3-opus, etc.
  - **Gemini**: gemini-1.5-pro, gemini-2.5-pro, etc.
  - **Ollama**: Any local model (no API key required)
- **Environment Variables**:  
  Provider-specific (see [Installation & Setup](#installation--setup))
- **Note**:  
  Only OpenAI and Ollama are tested by default.

---

## Internal Workflow

- **Crawling**:  
  `runesmith.crawler.collect_code_chunks()` and `find_extensions()` recursively scan the codebase, respecting `.gitignore` and blacklists.
- **Token Management**:  
  `runesmith.llm.count_tokens()` and `get_context_window()` manage token limits and context window warnings.
- **Doc Generation**:  
  Per-chunk LLM summarization, optional merging/polishing, and minimal doc updates.

---

## Dependency Management

- **Lockfile**:  
  `uv.lock` with SHA256 hashes for deterministic, secure, and reproducible Python environments.
- **Editable Install**:  
  For development, the main project is referenced as an editable install.
- **Key Packages**:
  - `ollama`, `openai`, `tiktoken`, `typer`, `questionary`, `rich`, `pydantic`, `httpx`, `requests`, `python-dotenv`, `pyyaml`, `pathspec`
- **Platform Support**:  
  Multiple wheel files per package for different Python versions and OS/architecture combinations.

---

## Project Structure

```
runesmith/
├── src/runesmith/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── crawler.py
│   └── llm.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── README.md
├── LICENSE
```

---

## Extensibility

- **Custom Providers**:  
  Add new LLM providers via the plugin interface.
- **Hooks**:  
  Pre/post-deployment hooks for IaC workflows.
- **Blueprints**:  
  Authored in `/blueprints` (YAML/JSON).
- **Examples/Docs**:  
  Provided in `/examples` and `/docs`.

---

## .gitignore Policy

- **Excludes**:
  - Python bytecode and cache files: `__pycache__/`, `*.pyc`, `*.pyo`
  - Build artifacts and distribution directories: `build/`, `dist/`, `wheels/`, `*.egg-info`
  - Virtual environment directories and environment files: `.venv`, `*.env`
  - Batch/config files: `batch*`, `config*`
  - Web directory and test script: `web/`, `test.py`
  - Cache files and directories: `cache*`
- **Purpose**:  
  Prevents version control of generated, environment-specific, and temporary files to maintain repository cleanliness.

---

## Versioning

- **Project Version**: 0.1.0
- **Python Version**: 3.10 (enforced via `.python-version`)

---

## License

**MIT License** © 2025 yail259

- Permission is granted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
- The software is provided "as is", without warranty of any kind.

---

## Changelog

### 0.1.0 (Initial Release)
- First public release.
- Multi-provider LLM support (OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama).
- Interactive CLI and YAML config-driven workflows.
- Per-chunk code summarization and doc synthesis.
- IaC blueprint authoring and deployment (experimental).
- Plugin-based extensibility for providers and workflows.
- Deterministic dependency management with `uv.lock`.
- Python 3.10 support.

---

## Planned Enhancements

- Add generated docs to LLM context for iterative updates.
- Retrieval-Augmented Generation (RAG) for large codebases.
- Standalone binary packaging.
- Multilanguage support.
- Iterative prompting/looping for improved doc quality.

---

## Contribution

- **Open Source**: MIT License.
- **Guidelines**: See `CONTRIBUTING.md` in the repository.

---

## Acknowledgements

- [uv](https://astral.sh/uv/), [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Questionary](https://github.com/tmbo/questionary), and other open-source Python packages.

---

**For detailed API documentation, CLI reference, and examples, see the `/docs` and `/examples` directories in the repository.**