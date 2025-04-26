# Runesmith User Guide

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
15. [Planned Enhancements](#planned-enhancements)
16. [Contribution](#contribution)
17. [Changelog](#changelog)

---

## 1. Core Functionality

- **Purpose**:  
  Runesmith automates the generation and updating of documentation for codebases or files using LLM APIs. It can also manage modular, composable infrastructure blueprints for cloud-agnostic deployments.
- **Modes**:  
  - **Interactive CLI Wizard**: Step-by-step guided setup.
  - **YAML Config-Driven**: Automated runs using a configuration file.
- **IaC Support**:  
  Author, compose, validate, and deploy infrastructure blueprints with version and state management.

---

## 2. Key Features

- **Automatic Documentation**: One-command generation/updating of READMEs, API docs, tutorials, quickstarts, and more.
- **Multi-Provider LLM Support**: OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama (local).
- **Context Awareness**: Honors `.gitignore`, blacklists, and existing documentation; makes minimal, safe changes.
- **Interactive & Config Modes**: Wizard-based or YAML config-driven workflows.
- **Customization**: Select doc types, blacklist file extensions, add custom LLM instructions.
- **Token Safety**: Warns if codebase exceeds LLM context window.
- **Extensibility**: Plugin-based architecture for providers and workflows.
- **IaC Blueprints**: Modular, declarative YAML/JSON blueprints for infrastructure.

---

## 3. Architecture

- **CLI**: Built with [Typer](https://typer.tiangolo.com/).
- **Modular/Plugin Design**: Easily extensible for new providers and workflows.
- **Declarative IaC**: YAML/JSON blueprints for infrastructure.
- **Provider SDK/CLI Integration**: For cloud operations.
- **State/Version Tracking**: For blueprints and deployments.

---

## 4. Installation & Setup

### Requirements

- **Python**: 3.10 (enforced via `.python-version`)
- **Platform**: Linux, macOS, Windows

### Install via PyPI

```bash
pip install runesmith
```

### Install from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/runesmith.git
   cd runesmith
   ```
2. **Install dependencies (recommended: [uv](https://astral.sh/uv/)):**
   ```bash
   uv sync
   ```
3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

### Environment Variables

- Store LLM provider credentials in a `.env` file or export them directly:
  - **OpenAI**: `OPENAI_API_KEY`
  - **Azure OpenAI**: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
  - **Anthropic**: `ANTHROPIC_API_KEY`
  - **Gemini**: `GEMINI_API_KEY`
  - **Ollama**: No key required (local)

---

## 5. Usage

### Interactive Mode

```bash
runesmith generate
```
- Guided prompts for provider/model, codebase path, output directory, blacklist, doc types, and custom instructions.

### Config-Driven Mode

```bash
runesmith generate --config config.yaml
```
- Use a YAML config file to specify all options.

#### Example `config.yaml`

```yaml
provider: openai
model: gpt-4o
code_path: ./src
output_dir: ./docs
blacklist: [".pyc", ".pyo", ".env"]
doc_types: ["readme", "api", "quickstart"]
custom_instructions: "Focus on clarity and conciseness."
```

---

## 6. CLI Reference

- **Entry Point**:  
  `runesmith generate [--config config.yaml]`

- **Workflow**:
  1. Crawl codebase (respects `.gitignore` and blacklist).
  2. Summarize code chunks via LLM.
  3. Write summaries to a temporary folder.
  4. Merge/polish as needed per doc type.
  5. Clean up.

- **Options**:
  - `--config, -c`: Path to YAML config file.

---

## 7. LLM Provider Integration

- **Supported Providers**:
  - **OpenAI**: gpt-4o, gpt-4-turbo, gpt-4.5, etc.
  - **Azure OpenAI**: gpt-4o, gpt-4-turbo, etc.
  - **Anthropic**: claude-3.5-haiku, claude-3-opus, etc.
  - **Gemini**: gemini-1.5-pro, gemini-2.5-pro, etc.
  - **Ollama**: Any local model (no API key required).

- **Environment Variables**:
  - See [Installation & Setup](#installation--setup).

- **Notes**:
  - Only OpenAI and Ollama are tested by default.
  - Provider/model selection is interactive or via config.

---

## 8. Internal Workflow

- **Crawling**:  
  Uses `.gitignore` and extension blacklist to filter files.
- **Token Management**:  
  Counts tokens, warns if context window is exceeded.
- **Documentation Generation**:  
  - Per-chunk LLM summarization.
  - Optional merging/polishing.
  - Minimal, safe updates to existing docs.
- **IaC Blueprints**:  
  Author, compose, validate, and deploy infrastructure as code.

---

## 9. Dependency Management

- **Lockfile**:  
  Uses `uv.lock` for reproducible installs (SHA256 hashes for all packages).
- **Editable Install**:  
  For development, install with `pip install -e .`.
- **Key Packages**:
  - `ollama`, `openai`, `tiktoken`, `typer`, `questionary`, `rich`, `pydantic`, `httpx`, `requests`, `python-dotenv`, `pyyaml`, `pathspec`
- **Reproducibility**:  
  All dependencies are pinned for deterministic builds.

---

## 10. Project Structure

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

## 11. Extensibility

- **Custom Providers**:  
  Add new LLM providers via plugin interface.
- **Hooks**:  
  Pre/post-deployment hooks for IaC workflows.
- **Blueprints**:  
  Authored in `/blueprints` (YAML/JSON).
- **Examples/Docs**:  
  Provided in `/examples` and `/docs`.

---

## 12. .gitignore Policy

- **Excludes**:
  - Python bytecode: `__pycache__/`, `*.pyc`, `*.pyo`
  - Build/dist artifacts: `build/`, `dist/`, `wheels/`, `*.egg-info`
  - Virtual environments: `.venv`
  - Environment files: `*.env`
  - Batch/config files: `batch*`, `config*`
  - Web directory: `web/`
  - Test scripts: `test.py`
  - Cache files: `cache*`
- **Purpose**:  
  Prevents version control of generated, environment-specific, and temporary files.

---

## 13. Versioning

- **Project Version**: 0.1.0
- **Python Version**: 3.10

---

## 14. License

**MIT License** © 2025 yail259

- Permission is granted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
- The software is provided "as is", without warranty of any kind.

See [LICENSE](./LICENSE) for the full text.

---

## 15. Planned Enhancements

- Add generated docs to LLM context for updates.
- Retrieval-Augmented Generation (RAG) for large codebases.
- Standalone binary packaging.
- Multilanguage support.
- Iterative prompting/looping.

---

## 16. Contribution

- **Open Source**: MIT License.
- **Guidelines**: See `CONTRIBUTING.md` in the repository.

---

## 17. Changelog

### 0.1.0 (2025-06-XX)
- Initial public release.
- Multi-provider LLM support: OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama.
- Interactive CLI wizard and YAML config-driven workflows.
- Per-chunk code summarization and document synthesis.
- IaC blueprint authoring and deployment (modular, declarative).
- Plugin-based extensibility for providers and workflows.
- `.gitignore` and blacklist support for codebase crawling.
- Minimal, safe updates to existing documentation.
- Token/context window management and warnings.
- Reproducible dependency management with `uv.lock`.
- MIT License.

---

## Appendix: Python API Usage

You can also use Runesmith as a Python module:

```python
import runesmith

# Example: Generate documentation programmatically
# (See API documentation for details)
```

---

## Appendix: Example CLI Session

```bash
$ runesmith generate
? Select LLM provider: OpenAI
? Select model: gpt-4o
? Codebase directory: ./src
? Output directory: ./docs
? Blacklist file extensions: .pyc, .env
? Documentation types: [x] README [x] API [ ] Tutorial [ ] Quickstart
? Custom LLM instructions: "Focus on clarity and conciseness."
? Save these settings to config.yaml? Yes
...
[Progress bars and output]
```

---

For more details, see the [API documentation](./docs/api_documentation.md) and [examples](./examples/).

---

**End of User Guide**