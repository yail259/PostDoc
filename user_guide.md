# User Guide: POSTDOC CLI Tool

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [CLI Usage](#cli-usage)
- [How POSTDOC Works](#how-postdoc-works)
- [Main Components](#main-components)
- [Documentation Generation Logic](#documentation-generation-logic)
- [Supported Documentation Types](#supported-documentation-types)
- [Model and Provider Support](#model-and-provider-support)
- [Respecting .gitignore and Blacklists](#respecting-gitignore-and-blacklists)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

**POSTDOC** is a command-line tool for generating and updating high-quality documentation for your codebase using OpenAI and other LLM providers. It can create or minimally update documentation such as READMEs, API docs, quickstart guides, and more, while respecting your `.gitignore` and existing documentation.

---

## Features

- **AI-powered documentation:** Uses OpenAI and other LLMs to generate or update documentation.
- **Minimal, safe changes:** If documentation already exists, POSTDOC will only update, proofread, and tweak it, preserving all critical information and avoiding unnecessary rewrites.
- **Interactive or config-driven:** Use a YAML config file or answer interactive prompts.
- **Respects `.gitignore`:** Only includes files not ignored by your `.gitignore`.
- **Customizable:** Choose which file types to skip, what documentation to generate, and add custom instructions for the language model.
- **Multiple LLM providers:** Supports OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local).

---

## Installation

### 1. Prerequisites

- **Python 3.10+** is required.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.

### 2. Install uv

Follow the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### 3. Install dependencies

From your project directory, run:

```sh
uv sync
```

This will install all required dependencies as specified in `pyproject.toml` and `uv.lock`.

### 4. Set up your OpenAI API key

Create a `.env` file in your project root with:

```
OPENAI_API_KEY=sk-...
```

Or set the environment variable in your shell.

---

## Configuration

POSTDOC can be configured via a YAML file or interactively.

### Supported Settings

- `code_path`: Path to the code directory or file.
- `output_dir`: Directory to save generated documentation.
- `blacklist`: List of file extensions to skip.
- `doc_types`: List of documentation types to generate (e.g., Readme, API documentation, Quickstart guide, etc.).
- `custom_instructions`: Custom instructions for the language model (optional).
- `model`: Model to use (e.g., "gpt-4.1").
- `provider`: LLM provider (e.g., "OpenAI", "AzureOpenAI", "Anthropic", "Gemini", "Ollama").

### Example `config.yaml`

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

## CLI Usage

Run POSTDOC from your project root:

```sh
python core/postdoc.py [-c CONFIG]
```

- `-c, --config`: Path to a YAML config file with settings.

If no config file is provided, POSTDOC will interactively prompt for all required settings.

---

## How POSTDOC Works

1. **Configuration:** Loads settings from a YAML file or prompts you interactively.
2. **Code Collection:** Gathers code from the specified path, respecting `.gitignore` and your blacklist.
3. **Token Counting:** Checks if the code and instructions fit within the selected model's context window.
4. **Documentation Generation:** For each selected documentation type:
    - If documentation already exists, it is updated with minimal, safe changes.
    - Otherwise, new documentation is generated.
5. **Output:** Each documentation type is saved as a Markdown file in the output directory.

---

## Main Components

### 1. `core/postdoc.py` (CLI Entrypoint)

- Loads configuration (YAML or interactive).
- Collects code, respecting `.gitignore` and blacklist.
- Checks token count against model context window.
- For each selected documentation type:
    - Generates or updates documentation using the selected LLM provider.
    - Writes output to a Markdown file in the output directory.

**Key Functions:**
- `load_config(path: str) -> dict`: Load YAML config.
- `prompt_user() -> dict`: Interactive prompt for settings.
- `write_to_file(filename: str, content: str)`: Write content to file.
- `main()`: Main CLI logic.

### 2. `core/crawler.py` (Codebase Crawling and Filtering)

- `load_gitignore(root: Path)`: Loads `.gitignore` as a pathspec.
- `is_ignored(fp: Path, spec, root: Path) -> bool`: Checks if a file is ignored.
- `find_extensions(dir_path: str) -> list[str]`: Returns all unique file extensions in a directory, respecting `.gitignore`.
- `collect_code(dir_path: str, blacklisted: list[str]) -> str`: Concatenates all non-blacklisted, non-ignored file contents into a single string, with file headers.

### 3. `core/llm.py` (LLM API and Token Counting)

- `check_context_window(model: str, instruct: str, prompt: str)`: Returns `(token_count, context_window, fallback_encoding)`. Raises `KeyError` if model is unknown.
- `generate_docs(model: str, instruct: str, prompt: str, provider: str, temperature: float) -> str`: Calls the selected LLM provider to generate documentation.
- `build_instruction(doc_type, custom_instruct, output_dir, code_path)`: Builds the system prompt, optionally including existing documentation for minimal updates.

---

## Documentation Generation Logic

- **Existing Documentation:** If documentation already exists, POSTDOC will update, proofread, and tweak it, making only minimal, safe changes. All critical information is preserved or replaced with equivalent, updated information.
- **No Major Rewrites:** Major rewrites or unnecessary alterations are not introduced.
- **New Documentation:** If no documentation exists, POSTDOC generates it from scratch.

---

## Supported Documentation Types

- Readme
- API documentation
- Quickstart guide
- Tutorial
- User guide
- Reference

---

## Model and Provider Support

- **Models:** Defined in `core/llm.py` (e.g., `"gpt-4.1": {"context_window": 1047576}`).
- **Providers:** OpenAI, AzureOpenAI, Anthropic, Gemini, Ollama (local).
- **Tokenization:** Uses `tiktoken` and falls back to a known encoding if the model is not recognized.
- **Provider Selection:** Choose provider interactively or via config.

---

## Respecting .gitignore and Blacklists

- All code collection respects `.gitignore` patterns.
- You can blacklist file extensions interactively or via config to skip certain files.

---

## Output

- Each documentation type is saved as a Markdown file in the output directory, named after the type (e.g., `api_documentation.md`).

---

## Troubleshooting

- **Python Version:** Ensure you are using Python 3.10+.
- **Dependencies:** Install all dependencies with `uv sync` after installing [uv](https://docs.astral.sh/uv/getting-started/installation/).
- **OpenAI Key:** Ensure your API key is set in `.env` or your environment.
- **Token Limit:** If you encounter token limit errors, reduce the amount of code or split documentation generation.
- **Provider Issues:** Only OpenAI and Ollama are tested; others may require additional setup.

---

## Contributing

Contributions are welcome! Please open issues or pull requests as needed.

---

## License

This project is licensed under the MIT License (see `LICENSE` file for details).

---

## Contact

For questions or support, please open an issue on GitHub or contact the repository maintainer.

---

**Happy documenting!** 🪄