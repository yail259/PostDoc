# Runesmith: Automated Code Documentation with LLMs

---

## Overview

**Runesmith** is a Python CLI tool for automated, high-quality codebase documentation generation and management using Large Language Models (LLMs) such as OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local). It supports both interactive wizard and YAML config-driven workflows, and can also manage modular, composable infrastructure-as-code (IaC) blueprints for cloud-agnostic deployments.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quickstart](#quickstart)
4. [Configuration](#configuration)
5. [Supported LLM Providers & Models](#supported-llm-providers--models)
6. [Internal Workflow](#internal-workflow)
7. [Extensibility & Architecture](#extensibility--architecture)
8. [Project Structure](#project-structure)
9. [Dependency Management](#dependency-management)
10. [Versioning & Changelog](#versioning--changelog)
11. [Planned Enhancements](#planned-enhancements)
12. [Contribution](#contribution)
13. [License](#license)

---

## Features

- **Automatic Documentation**: One-command generation and updating of documentation (READMEs, API docs, tutorials, quickstarts, etc.).
- **Multi-Provider LLM Support**: OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local).
- **Context Awareness**: Honors `.gitignore`, blacklists, and existing documentation; makes minimal, safe changes.
- **Interactive & Config Modes**: Use an interactive CLI wizard or YAML config for repeatable runs.
- **Customization**: Select doc types, blacklist file extensions, add custom LLM instructions.
- **Token Safety**: Warns if codebase exceeds LLM context window.
- **IaC Blueprints**: Author, compose, validate, and deploy infrastructure blueprints with version/state management.
- **Extensible**: Plugin-based architecture for providers and workflows.

---

## Installation

### Requirements

- **Python**: 3.10 (enforced via `.python-version`)
- **Platform**: Linux, macOS, or Windows

### Install via PyPI

```bash
pip install runesmith
```

### Install from Source (with [uv](https://astral.sh/uv/))

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/runesmith.git
    cd runesmith
    ```
2. Install dependencies:
    ```bash
    uv sync
    ```
3. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

---

## Quickstart

### 1. Set Up Environment Variables

Set your LLM provider API keys as environment variables or in a `.env` file in your project root:

- **OpenAI**: `OPENAI_API_KEY`
- **Azure OpenAI**: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Gemini**: `GEMINI_API_KEY`
- **Ollama**: No key required (local)

### 2. Generate Documentation

#### Interactive Mode

```bash
runesmith generate
```
- Walks you through provider/model selection, codebase path, output directory, blacklist, doc types, and custom instructions.

#### Config-Driven Mode

1. Create a `config.yaml` (see [Configuration](#configuration) below).
2. Run:
    ```bash
    runesmith generate --config config.yaml
    ```

---

## Configuration

A sample `config.yaml`:

```yaml
provider: openai
model: gpt-4o
code_path: ./src
output_dir: ./docs
blacklist:
  - .pyc
  - .pyo
  - .md
doc_types:
  - readme
  - api
  - quickstart
custom_instructions: |
  Please generate concise, developer-friendly documentation.
```

**Configurable Options:**
- `provider`: LLM provider (openai, azure, anthropic, gemini, ollama)
- `model`: Model name (e.g., gpt-4o, claude-3.5-haiku)
- `code_path`: Path to codebase
- `output_dir`: Where to write docs
- `blacklist`: List of file extensions to skip
- `doc_types`: List of documentation types to generate
- `custom_instructions`: Additional instructions for the LLM

---

## Supported LLM Providers & Models

- **OpenAI**: gpt-4o, gpt-4-turbo, gpt-4.5, etc.
- **Azure OpenAI**: gpt-4o, gpt-4-turbo, etc.
- **Anthropic**: claude-3.5-haiku, claude-3-opus, etc.
- **Gemini**: gemini-1.5-pro, gemini-2.5-pro, etc.
- **Ollama**: Any local model (no API key required)

> *Note: Only OpenAI and Ollama are tested by default.*

---

## Internal Workflow

1. **Crawl Codebase**: Recursively scans the codebase, respecting `.gitignore` and blacklist.
2. **Token Management**: Counts tokens, warns if context window is exceeded.
3. **Per-Chunk Summarization**: Sends code chunks and instructions to the selected LLM provider.
4. **Doc Synthesis**: Merges and polishes chunk summaries into final documentation per selected type.
5. **Minimal Updates**: Updates existing docs minimally and safely.
6. **Output**: Writes documentation files to the specified output directory.

---

## Extensibility & Architecture

- **CLI**: Built with [Typer](https://typer.tiangolo.com/).
- **Plugin-Based**: Easily add new LLM providers or workflows.
- **Declarative IaC**: YAML/JSON blueprints for infrastructure, with version/state tracking.
- **Provider SDK/CLI Integration**: For cloud operations.
- **Hooks**: Pre/post-deployment for IaC.
- **Blueprints**: Authored in `/blueprints` (YAML/JSON).
- **Examples/Docs**: In `/examples` and `/docs`.

---

## Project Structure

```
runesmith/
├── src/runesmith/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── crawler.py
│   ├── llm.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── README.md
├── LICENSE
```

---

## Dependency Management

- **Lockfile**: `uv.lock` with SHA256 hashes for reproducible installs.
- **Editable Install**: For development.
- **Key Packages**: `ollama`, `openai`, `tiktoken`, `typer`, `questionary`, `rich`, `pydantic`, `httpx`, `requests`, `python-dotenv`, `pyyaml`, `pathspec`.
- **Platform Support**: Wheels for all major OS/architectures.
- **Security**: All dependencies are hash-pinned for integrity.

---

## Versioning & Changelog

### Version: 0.1.0

#### Changelog

- Initial public release.
- Multi-provider LLM support (OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama).
- Interactive CLI and YAML config-driven workflows.
- Per-chunk code summarization and doc synthesis.
- IaC blueprint authoring, validation, and deployment.
- Plugin-based provider/workflow extensibility.
- `.gitignore` and blacklist support.
- Minimal, safe doc updates.
- Token/context window management and warnings.
- Reproducible dependency management with `uv.lock`.
- MIT License.

---

## Planned Enhancements

- Add generated docs to LLM context for iterative updates.
- Retrieval-Augmented Generation (RAG) for large codebases.
- Standalone binary packaging.
- Multilanguage support.
- Iterative prompting/looping.

---

## Contribution

- **Open Source**: MIT License.
- **Guidelines**: See `CONTRIBUTING.md` in the repository.

---

## License

**MIT License © 2025 yail259**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## .gitignore Policy

- Excludes Python bytecode, build/dist artifacts, venvs, env files, batch/config files, `web/`, `test.py`, and cache files.
- Purpose: Prevents version control of generated, environment-specific, and temporary files to maintain repository cleanliness.

---

## Questions?

See the [examples](./examples), [docs](./docs), or open an issue on GitHub.

---

**End of Quickstart Guide**