# POSTDOC API Documentation

## Overview

**POSTDOC** is a CLI tool for generating and updating documentation for codebases or single files using OpenAI's API. It supports interactive configuration, YAML-based config files, and respects `.gitignore` patterns when collecting code. The tool is designed to update, proofread, and tweak existing documentation with minimal, safe changes, preserving all critical information.

---

## Installation

**Dependencies:**  
POSTDOC uses Python 3.10+ and requires several dependencies managed via [uv](https://docs.astral.sh/uv/getting-started/installation/).

**To install all dependencies:**
1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run in your project directory:
   ```sh
   uv sync
   ```

---

## CLI Usage

```sh
python core/postdoc.py [-c CONFIG]
```

- `-c, --config`: Path to a YAML config file with settings.

If no config file is provided, POSTDOC will interactively prompt for all required settings.

---

## Configuration

POSTDOC can be configured via a YAML file or interactively. The following settings are supported:

- `code_path`: Path to the code directory or file.
- `output_dir`: Directory to save generated documentation.
- `blacklist`: List of file extensions to skip.
- `doc_types`: List of documentation types to generate (e.g., Readme, API documentation, Quickstart guide, etc.).
- `custom_instructions`: Custom instructions for the language model (optional).
- `model`: Model to use (e.g., "gpt-4.1").

Example `config.yaml`:
```yaml
code_path: ./src
output_dir: ./docs
blacklist: [".test", ".md"]
doc_types: ["Readme", "API documentation"]
custom_instructions: "Add company-specific style."
model: "gpt-4.1"
```

---

## Main Components

### 1. `core/postdoc.py`

**Entrypoint for the CLI tool.**

- Loads configuration (YAML or interactive).
- Collects code, respecting `.gitignore` and blacklist.
- Checks token count against model context window.
- For each selected documentation type:
  - Generates or updates documentation using OpenAI.
  - Writes output to a Markdown file in the output directory.

**Key Functions:**
- `load_config(path: str) -> dict`: Load YAML config.
- `prompt_user() -> dict`: Interactive prompt for settings.
- `write_to_file(filename: str, content: str)`: Write content to file.
- `main()`: Main CLI logic.

### 2. `core/crawler.py`

**Codebase crawling and filtering.**

- `load_gitignore(root: Path)`: Loads `.gitignore` as a pathspec.
- `is_ignored(fp: Path, spec, root: Path) -> bool`: Checks if a file is ignored.
- `find_extensions(dir_path: str) -> list[str]`: Returns all unique file extensions in a directory, respecting `.gitignore`.
- `collect_code(dir_path: str, blacklisted: list[str]) -> str`: Concatenates all non-blacklisted, non-ignored file contents into a single string, with file headers.

### 3. `core/llm.py`

**OpenAI API and token counting.**

- `check_context_window(model: str, instruct: str, prompt: str)`: Returns `(token_count, context_window, fallback_encoding)`. Raises `KeyError` if model is unknown.
- `generate_docs(model: str, instruct: str, prompt: str) -> str`: Calls OpenAI API to generate documentation.

---

## Documentation Generation Logic

- If documentation already exists, POSTDOC will update, proofread, and tweak it, making only minimal, safe changes.
- All critical information is preserved or replaced with equivalent, updated information.
- **IMPORTANT:** Major rewrites or unnecessary alterations are not introduced.

---

## Supported Documentation Types

- Readme
- API documentation
- Quickstart guide
- Tutorial
- User guide
- Reference

---

## Model Support

- Models and their context window sizes are defined in `core/llm.py` (e.g., `"gpt-4.1": {"context_window": 1047576}`).
- Tokenization uses `tiktoken` and falls back to a known encoding if the model is not recognized.

---

## Respecting .gitignore and Blacklists

- All code collection respects `.gitignore` patterns.
- You can blacklist file extensions interactively or via config to skip certain files.

---

## Output

- Each documentation type is saved as a Markdown file in the output directory, named after the type (e.g., `api_documentation.md`).

---

## License

This project is licensed under the MIT License (see `LICENSE` file for details).

---

## Troubleshooting

- Ensure you are using Python 3.10+.
- Install all dependencies with `uv sync` after installing [uv](https://docs.astral.sh/uv/getting-started/installation/).
- If you encounter token limit errors, reduce the amount of code or split documentation generation.

---

## Contributing

Contributions are welcome! Please open issues or pull requests as needed.

---

## Contact

For questions or support, please contact the repository maintainer.

---

**End of API Documentation**