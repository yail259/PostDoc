Below is an **updated and expanded Tutorial** for the POSTDOC tool, designed to be clear, practical, and developer-focused. It covers installation, configuration, usage, troubleshooting, and advanced tips, and is suitable for inclusion as a `TUTORIAL.md` or as a section in your documentation.

---

# POSTDOC Tutorial

**Effortlessly generate and update high-quality documentation for your codebase using AI.**

---

## What is POSTDOC?

POSTDOC is a command-line tool that uses OpenAI (and other LLM providers) to generate or update documentation for your codebase. It can create new docs (like README, API docs, tutorials, etc.) or minimally update existing ones, always preserving critical information and respecting your `.gitignore`.

---

## 1. Installation

### Prerequisites

- **Python 3.10+**  
  Check your version:
  ```sh
  python3 --version
  ```

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** (for dependency management)  
  Install via [official instructions](https://docs.astral.sh/uv/getting-started/installation/).

### Install Dependencies

From your project directory:

```sh
uv sync
```

This will install all required dependencies as specified in `pyproject.toml` and `uv.lock`.

---

## 2. Set Up Your OpenAI API Key

POSTDOC needs access to the OpenAI API (or other LLM providers).

- **Create a `.env` file** in your project root:
  ```
  OPENAI_API_KEY=sk-...
  ```
- Or set the environment variable in your shell:
  ```sh
  export OPENAI_API_KEY=sk-...
  ```

---

## 3. Quickstart: Generate Documentation

### Run POSTDOC

```sh
python3 core/postdoc.py
```

- **Interactive mode:**  
  You'll be prompted for all settings (code path, output dir, file types to skip, doc types, model, etc.).
- **Config file mode:**  
  Save your settings to a YAML file and run:
  ```sh
  python3 core/postdoc.py --config config.yaml
  ```

---

## 4. Configuration

You can configure POSTDOC either **interactively** or via a **YAML config file**.

### Example `config.yaml`

```yaml
code_path: ./src
output_dir: ./docs
blacklist: [".test", ".md"]
doc_types: ["Readme", "API documentation", "Quickstart guide"]
custom_instructions: "Add company-specific style."
model: "gpt-4.1"
provider: "OpenAI"
```

**Config fields:**

- `code_path`: Path to your code directory or file.
- `output_dir`: Where to save generated docs.
- `blacklist`: List of file extensions to skip (e.g., `.test`, `.md`).
- `doc_types`: List of documentation types to generate.
- `custom_instructions`: (Optional) Extra instructions for the LLM.
- `model`: LLM model to use (e.g., `gpt-4.1`).
- `provider`: LLM provider (`OpenAI`, `AzureOpenAI`, `Anthropic`, `Gemini`, `Ollama`).

---

## 5. How POSTDOC Works

1. **Collects code** from your project, respecting `.gitignore` and your blacklist.
2. **Checks token limits** for your selected LLM model.
3. For each selected documentation type:
   - **If doc exists:** Updates/proofreads/tweaks it, making only minimal, safe changes.
   - **If doc does not exist:** Generates it from scratch.
4. **Saves** each doc as a Markdown file in your output directory.

**Supported doc types:**
- Readme
- API documentation
- Quickstart guide
- Tutorial
- User guide
- Reference

---

## 6. Advanced Usage

### Excluding Files

- POSTDOC always respects your `.gitignore`.
- You can also blacklist file extensions interactively or via config.

### Customizing LLM Provider

- By default, POSTDOC uses OpenAI.
- You can select other providers (AzureOpenAI, Anthropic, Gemini, Ollama) if you have API keys/configured endpoints.

### Minimal, Safe Updates

- If a documentation file already exists, POSTDOC will **not** rewrite it from scratch.
- It will only proofread, update, and tweak, preserving all critical information.

---

## 7. Project Structure

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

## 8. Troubleshooting

- **Dependency issues:**  
  Make sure you have installed [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync`.

- **OpenAI errors:**  
  Ensure your API key is set in `.env` or your environment.

- **Token limit exceeded:**  
  Try excluding more file types or splitting your codebase.

- **Unknown model:**  
  Check that your model name matches one in `core/llm.py`.

- **Provider errors:**  
  Make sure you have the correct API keys and environment variables for your chosen provider.

---

## 9. Tips & Best Practices

- **Start with a small codebase** to test POSTDOC and see how it updates docs.
- **Review generated docs** before publishing—POSTDOC aims for safety, but always check!
- **Use custom instructions** to enforce your company or project style.
- **Save your config** for repeatable, consistent documentation runs.

---

## 10. Contributing

Contributions are welcome! Please open issues or pull requests.

---

## 11. License

This project is licensed under the [MIT License](LICENSE).

---

## 12. Contact

For questions or support, please open an issue on GitHub.

---

**Happy documenting!** 🪄

---

## Appendix: Example Workflow

1. **Initialize your project and codebase.**
2. **Add a `.gitignore`** to exclude files you don't want documented.
3. **Run POSTDOC** and follow the prompts, or create a `config.yaml`.
4. **Check the generated docs** in your output directory.
5. **Edit or rerun** as needed, tweaking blacklist or instructions.
6. **Commit your docs** to version control.

---

**End of Tutorial**