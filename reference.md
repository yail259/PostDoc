# POSTDOC Reference

This document provides a detailed technical reference for the **POSTDOC** CLI tool, its architecture, and its Python API. It is intended for developers who want to understand, extend, or integrate POSTDOC.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [CLI Usage](#cli-usage)
- [Configuration](#configuration)
- [Python API Reference](#python-api-reference)
  - [core/postdoc.py](#corepostdocpy)
  - [core/crawler.py](#corecrawlerpy)
  - [core/llm.py](#corellmpy)
- [Supported LLM Providers](#supported-llm-providers)
- [Extending POSTDOC](#extending-postdoc)
- [Error Handling](#error-handling)
- [Environment Variables](#environment-variables)
- [File Structure](#file-structure)
- [License](#license)

---

## Overview

**POSTDOC** is a Python 3.10+ CLI tool for generating and updating documentation for codebases or single files using LLMs (OpenAI, Azure, Anthropic, Gemini, Ollama). It supports interactive configuration, YAML-based config files, and respects `.gitignore` and extension blacklists. POSTDOC is designed to update existing documentation with minimal, safe changes, preserving all critical information.

---

## Architecture

POSTDOC is organized into three main modules:

- **core/postdoc.py**: CLI entry point, user interaction, orchestration.
- **core/crawler.py**: Codebase crawling, `.gitignore`/blacklist handling.
- **core/llm.py**: LLM API abstraction, token counting, prompt construction.

---

## CLI Usage

```sh
python core/postdoc.py [-c CONFIG]
```

- `-c, --config`: Path to a YAML config file. If omitted, prompts interactively.

---

## Configuration

POSTDOC can be configured via a YAML file or interactively. Supported settings:

| Key                 | Type         | Description                                                                 |
|---------------------|--------------|-----------------------------------------------------------------------------|
| `code_path`         | str          | Path to code directory or file.                                             |
| `output_dir`        | str          | Directory to save generated documentation.                                  |
| `blacklist`         | list[str]    | List of file extensions to skip (e.g., [".md", ".test"]).                   |
| `doc_types`         | list[str]    | Documentation types to generate (e.g., ["Readme", "API documentation"]).    |
| `custom_instructions` | str        | Custom instructions for the LLM (optional).                                 |
| `model`             | str          | Model name (e.g., "gpt-4.1").                                               |
| `provider`          | str          | LLM provider ("OpenAI", "AzureOpenAI", "Anthropic", "Gemini", "Ollama").    |

**Example config.yaml:**
```yaml
code_path: ./src
output_dir: ./docs
blacklist: [".test", ".md"]
doc_types: ["Readme", "API documentation"]
custom_instructions: "Add company-specific style."
model: "gpt-4.1"
provider: "OpenAI"
```

---

## Python API Reference

### core/postdoc.py

**Entrypoint and Orchestration**

- `load_config(path: str) -> dict`
  - Load YAML config from file.

- `prompt_user() -> dict`
  - Interactive prompt for all settings. Returns config dict.

- `write_to_file(filename: str, content: str)`
  - Write string content to file.

- `main()`
  - Main CLI logic: loads config, collects code, checks token limits, generates docs, writes output.

**CLI Flow:**
1. Load config (YAML or interactive).
2. Collect code (respects `.gitignore` and blacklist).
3. Check token count vs. model context window.
4. For each doc type:
   - Build instruction (see `llm.build_instruction`).
   - Generate documentation via `llm.generate_docs`.
   - Write output to Markdown file in output directory.

---

### core/crawler.py

**Codebase Crawling and Filtering**

- `load_gitignore(root: Path) -> pathspec.PathSpec | None`
  - Loads `.gitignore` from root directory.

- `is_ignored(fp: Path, spec, root: Path) -> bool`
  - Returns True if file is ignored by `.gitignore`.

- `find_extensions(dir_path: str) -> list[str]`
  - Returns sorted list of unique file extensions in directory, respecting `.gitignore`.

- `collect_code(dir_path: str, blacklisted: list[str]) -> str`
  - Concatenates all non-blacklisted, non-ignored file contents into a single string, with file headers.

---

### core/llm.py

**LLM API, Token Counting, Prompt Construction**

- `models: dict`
  - Maps model names to context window sizes, e.g.:
    ```python
    models = {
        "gpt-4.1": {"context_window": 1047576},
        "phi4": {"context_window": 16000},
    }
    ```

- `unwrap_markdown_block(text: str) -> str`
  - Removes surrounding ```markdown code fences if present.

- `check_context_window(model: str, instruct: str, prompt: str) -> (int, int, str|None)`
  - Returns (token_count, context_window, fallback_encoding). Raises KeyError if model unknown.

- `build_instruction(doc_type: str, custom_instruct: str, output_dir: str, code_path: str) -> str`
  - Constructs the instruction string for the LLM. If the output file exists and is not under `code_path`, its contents are appended for minimal update.

- `generate_docs(model: str, instruct: str, prompt: str, *, provider: str|None = None, temperature: float = 0.0) -> str`
  - Calls the selected LLM provider to generate documentation. Supported providers: `"openai"`, `"azureopenai"`, `"anthropic"`, `"google"`, `"ollama"`. Returns the generated documentation as a string.

---

## Supported LLM Providers

POSTDOC supports the following LLM providers (via `core/llm.py`):

- **OpenAI** (`openai`)
- **Azure OpenAI** (`azureopenai`)
- **Anthropic** (`anthropic`)
- **Google Gemini** (`google`)
- **Ollama** (`ollama`)

Provider selection is via config or the `LLM_PROVIDER` environment variable.

---

## Extending POSTDOC

- **Add a new provider:**  
  Implement a `_generate_<provider>()` function in `llm.py` and add it to the `_GENERATORS` dict.
- **Add a new documentation type:**  
  Add the type to the `doc_types` list in config or prompt. The output file will be named `<type>.md` (spaces replaced with underscores).
- **Custom prompt logic:**  
  Modify `build_instruction()` in `llm.py` for advanced prompt engineering.

---

## Error Handling

- **Unknown model:**  
  Raises `KeyError` in `check_context_window`.
- **Token limit exceeded:**  
  Exits with error if code + prompt exceeds model context window.
- **Provider errors:**  
  Raises `ValueError` if provider is not supported.

---

## Environment Variables

- `OPENAI_API_KEY` – OpenAI API key (required for OpenAI/Azure).
- `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION` – For Azure OpenAI.
- `ANTHROPIC_API_KEY` – For Anthropic.
- `GOOGLE_API_KEY` – For Gemini.
- `LLM_PROVIDER` – Default provider if not set in config.

---

## File Structure

```
core/
  postdoc.py      # Main CLI entry point
  crawler.py      # Code collection and .gitignore handling
  llm.py          # LLM API and token counting
pyproject.toml    # Project metadata and dependencies
uv.lock           # Locked dependency versions
config.yaml       # (Optional) Saved configuration
```

---

## License

POSTDOC is licensed under the MIT License. See the `LICENSE` file for details.

---

**End of Reference**