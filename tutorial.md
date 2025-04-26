# Runesmith: Automated Code Documentation with LLMs

---

## Overview

**Runesmith** is a Python CLI tool for automated, high-quality codebase documentation generation and management using Large Language Models (LLMs) such as OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local). It supports both interactive wizard-driven and YAML configuration-driven workflows, and is designed for extensibility, reproducibility, and cloud-agnostic infrastructure-as-code (IaC) blueprints.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
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

## Features

- **Automatic Documentation**: One-command generation and updating of documentation (READMEs, API docs, tutorials, quickstarts, etc.).
- **Multi-Provider LLM Support**: Integrates with OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local, no API key required).
- **Context Awareness**: Honors `.gitignore`, blacklists, and existing documentation; makes minimal, safe changes.
- **Interactive & Config Modes**: Use an interactive CLI wizard or YAML config files.
- **Customization**: Select doc types, blacklist file extensions, and add custom LLM instructions.
- **Token Safety**: Warns if codebase exceeds LLM context window.
- **IaC Blueprints**: Modular, composable infrastructure blueprints for cloud-agnostic deployments.
- **Extensibility**: Plugin-based architecture for providers and workflows.

---

## Architecture

- **CLI**: Built with [Typer](https://typer.tiangolo.com/).
- **Modular/Plugin Design**: Easily extendable for new providers and workflows.
- **Declarative IaC**: YAML/JSON blueprints for infrastructure.
- **Provider SDK/CLI Integration**: For cloud operations.
- **State/Version Tracking**: For blueprints and deployments.

---

## Installation

### Requirements

- **Python 3.10** (enforced via `.python-version`)
- [uv](https://astral.sh/uv/) (recommended for dependency management and reproducible installs)

### Install via PyPI

```bash
pip install runesmith
```

### Install from Source

```bash
git clone https://github.com/yourusername/runesmith.git
cd runesmith
uv sync
source .venv/bin/activate
```

---

## Quick Start

### Interactive Mode

```bash
runesmith generate
```

### Config-Driven Mode

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
  - readme
  - api
  - tutorial
custom_instruct: "Focus on clarity and conciseness."
```

---

## Configuration

- **Provider/Model**: Choose from supported LLM providers and models.
- **Code Path**: Directory to scan for code.
- **Output Directory**: Where generated docs are written.
- **Blacklist**: List of file extensions to ignore.
- **Doc Types**: Select which documentation types to generate.
- **Custom Instructions**: Additional instructions for the LLM.

Configuration can be provided interactively or via a YAML file.

---

## CLI Reference

### Entry Point

```bash
runesmith generate [--config config.yaml]
```

### Workflow

1. **Crawl codebase** (respects `.gitignore` and blacklist).
2. **Summarize code chunks** via LLM.
3. **Write summaries** to a temporary folder.
4. **Merge/polish** as needed per doc type.
5. **Clean up** temporary files.

---

## LLM Provider Integration

- **Supported Providers**: OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama (local).
- **Model Examples**:
  - OpenAI: `gpt-4o`, `gpt-4-turbo`
  - Azure OpenAI: `gpt-4o`, `gpt-4-turbo`
  - Anthropic: `claude-3.5-haiku`, `claude-3-opus`
  - Gemini: `gemini-1.5-pro`, `gemini-2.5-pro`
  - Ollama: Any local model (no API key required)
- **Environment Variables**:
  - OpenAI: `OPENAI_API_KEY`
  - Azure OpenAI: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
  - Anthropic: `ANTHROPIC_API_KEY`
  - Gemini: `GEMINI_API_KEY`
  - Ollama: No key needed
- **.env Support**: Place credentials in a `.env` file at the project root.

---

## Internal Workflow

- **Crawling**: Uses `.gitignore` and blacklist to collect code chunks.
- **Token Management**: Counts tokens, warns if context window is exceeded.
- **Doc Generation**: Per-chunk LLM summarization, optional merging/polishing, minimal doc updates.
- **IaC Blueprints**: Author, compose, validate, and deploy infrastructure blueprints with version/state management.

---

## Dependency Management

- **Lockfile**: Uses `uv.lock` with SHA256 hashes for reproducible installs.
- **Editable Install**: For development.
- **Key Packages**:
  - `ollama`, `openai`, `tiktoken`, `typer`, `questionary`, `rich`, `pydantic`, `httpx`, `requests`, `python-dotenv`, `pyyaml`, `pathspec`
- **Platform Support**: Wheels for all major OS/architectures.
- **Security**: All dependencies are hash-pinned for integrity.

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
└── examples/
```

---

## Extensibility

- **Custom Providers**: Add via plugin interface.
- **Hooks**: Pre/post-deployment for IaC.
- **Blueprints**: Authored in `/blueprints` (YAML/JSON).
- **Examples/Docs**: In `/examples` and `/docs`.

---

## .gitignore Policy

- **Excludes**:
  - Python bytecode: `__pycache__/`, `*.pyc`, `*.pyo`
  - Build/dist artifacts: `build/`, `dist/`, `wheels/`, `*.egg-info`
  - Virtual environments: `.venv`
  - Environment files: `*.env`
  - Batch/config files: `batch*`, `config*`
  - Web directory: `web/`
  - Test scripts: `test.py`
  - Cache files: `cache*`
- **Purpose**: Keeps repository clean by ignoring generated, environment-specific, and temporary files.

---

## Versioning

- **Project Version**: 0.1.0
- **Python Version**: 3.10

---

## License

**MIT License** © 2025 yail259

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Changelog

### 0.1.0 (2025-06-XX)
- Initial public release.
- Multi-provider LLM support (OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama).
- Interactive CLI wizard and YAML config-driven workflows.
- Per-chunk code summarization and doc synthesis.
- IaC blueprint authoring, validation, and deployment.
- Plugin-based provider/workflow extensibility.
- Reproducible dependency management with `uv.lock`.
- .gitignore and blacklist support for code crawling.
- Minimal/safe doc updates; context window/token management.
- MIT License.

---

## Planned Enhancements

- Add generated docs to LLM context for incremental updates.
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

- [uv](https://astral.sh/uv/)
- [Typer](https://typer.tiangolo.com/)
- [Rich](https://rich.readthedocs.io/)
- [Questionary](https://github.com/tmbo/questionary/)
- [OpenAI](https://openai.com/)
- [Ollama](https://ollama.com/)
- And all other open-source Python packages used.

---

For detailed API documentation, examples, and advanced usage, see the `/docs` and `/examples` directories in the repository.