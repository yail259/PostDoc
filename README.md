# POSTDOC API Documentation

## Overview

**POSTDOC** is a CLI tool for generating and updating documentation for codebases or single files using OpenAI's API and other LLM providers. It supports both interactive configuration and YAML-based config files, and respects `.gitignore` patterns and file blacklists when collecting code. POSTDOC is designed to update, proofread, and tweak existing documentation with minimal, safe changes, always preserving all critical information.

---

## Installation

**Dependencies:**  
POSTDOC requires Python 3.10+ and uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.

**To install all dependencies:**

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. In your project directory, run:
   ```sh
   uv sync
   ```

---

## CLI Usage

```sh
python3 core/postdoc.py [-c CONFIG]
```

- `-c, --config`: Path to a YAML config file. If omitted, POSTDOC will prompt interactively for all settings.

---

## Configuration

POSTDOC can be configured via a YAML file or interactively. Supported settings:

| Key                   | Type      | Description                                                              |
| --------------------- | --------- | ------------------------------------------------------------------------ |
| `code_path`           | str       | Path to code directory or file.                                          |
| `output_dir`          | str       | Directory to save generated documentation.                               |
| `blacklist`           | list[str] | List of file extensions to skip (e.g., [".md", ".test"]).                |
| `doc_types`           | list[str] | Documentation types to generate (e.g., ["Readme", "API documentation"]). |
| `custom_instructions` | str       | Custom instructions for the LLM (optional).                              |
| `model`               | str       | Model name (e.g., "gpt-4.1").                                            |
| `provider`            | str       | LLM provider ("OpenAI", "AzureOpenAI", "Anthropic", "Gemini", "Ollama"). |

**Example `config.yaml`:**

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

## TODOs

- [ ] add generated document to context window???
- [ ] add RAG system for context window issue
- [ ] package into binary?
- [ ] multilanguage support?

---

## API Reference

### core/postdoc.py

**Entrypoint and Orchestration**

- `load_config(path: str) -> dict`  
  Load YAML config from file.

- `prompt_user() -> dict`  
  Interactive prompt for all settings. Returns config dict.

- `write_to_file(filename: str, content: str)`  
  Write string content to file.

- `main()`  
  Main CLI logic: loads config, collects code, checks token limits, generates docs, writes output.

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
  Loads `.gitignore` from root directory.

- `is_ignored(fp: Path, spec, root: Path) -> bool`  
  Returns True if file is ignored by `.gitignore`.

- `find_extensions(dir_path: str) -> list[str]`  
  Returns sorted list of unique file extensions in directory, respecting `.gitignore`.

- `collect_code(dir_path: str, blacklisted: list[str]) -> str`  
  Concatenates all non-blacklisted, non-ignored file contents into a single string, with file headers.

---

### core/llm.py

**LLM API, Token Counting, Prompt Construction**

- `PROVIDER_MODELS: dict`  
  Maps provider/model names to context window sizes, e.g.:

  ```python
  PROVIDER_MODELS = {
      "OpenAI": {
          "gpt-4.1": 1_000_000,
          ...
      },
      ...
  }
  ```

- `unwrap_markdown_block(text: str) -> str`  
  Removes surrounding ```markdown code fences if present.

- `check_context_window(provider: str, model: str, instruct: str, prompt: str) -> (int, int, str|None)`  
  Returns (token_count, context_window, fallback_encoding). Raises KeyError if model unknown.

- `build_instruction(doc_type: str, custom_instruct: str, output_dir: str, code_path: str) -> str`  
  Constructs the instruction string for the LLM. If the output file exists and is not under `code_path`, its contents are appended for minimal update.

- `generate_docs(model: str, instruct: str, prompt: str, *, provider: str|None = None, temperature: float = 0.0) -> str`  
  Calls the selected LLM provider to generate documentation. Supported providers: `"openai"`, `"azureopenai"`, `"anthropic"`, `"google"`, `"ollama"`. Returns the generated documentation as a string.

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

## Updating Existing Documentation

If documentation already exists, POSTDOC will:

- Update, proofread, and tweak it, making only minimal, safe changes.
- Preserve all critical information or replace with equivalent, updated information.
- **IMPORTANT:** It will NOT introduce major rewrites or alter content unnecessarily.

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
- `GEMINI_API_KEY` – For Gemini.
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

**End of API Documentation**
