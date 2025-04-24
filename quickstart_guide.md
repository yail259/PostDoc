Here is a high-quality, up-to-date **Quickstart Guide** for POSTDOC, tailored for developers. This guide is concise, actionable, and covers the essential steps to get started, including installation, configuration, and usage.

---

# Quickstart Guide: POSTDOC

**POSTDOC** is a CLI tool for generating and updating high-quality documentation for your codebase using OpenAI and other LLM providers. It supports interactive setup, YAML config files, and respects `.gitignore` and file blacklists.

---

## 1. Prerequisites

- **Python 3.10+**  
  Check your version:
  ```sh
  python3 --version
  ```

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** (for dependency management)  
  Install via the [official instructions](https://docs.astral.sh/uv/getting-started/installation/).

---

## 2. Install Dependencies

From your project directory, run:

```sh
uv sync
```

This will install all required dependencies as specified in `pyproject.toml` and `uv.lock`.

---

## 3. Set Up Your OpenAI API Key

POSTDOC uses the OpenAI API (or other providers).  
Create a `.env` file in your project root with:

```
OPENAI_API_KEY=sk-...
```

Or set the environment variable in your shell.

---

## 4. Run POSTDOC

You can run POSTDOC interactively or with a config file.

**Interactive mode:**
```sh
python3 core/postdoc.py
```

**With a config file:**
```sh
python3 core/postdoc.py --config config.yaml
```

---

## 5. Configuration

You can configure POSTDOC either interactively or by creating a `config.yaml` file.

**Example `config.yaml`:**
```yaml
code_path: ./src
output_dir: ./docs
blacklist: [".test", ".md"]
doc_types: ["Readme", "API documentation", "Quickstart guide"]
custom_instructions: "Add company-specific style."
model: "gpt-4.1"
provider: "OpenAI"
```

**Config options:**
- `code_path`: Path to your code directory or file.
- `output_dir`: Where to save generated docs.
- `blacklist`: List of file extensions to skip.
- `doc_types`: Documentation types to generate (e.g., Readme, API documentation, Quickstart guide, etc.).
- `custom_instructions`: (Optional) Extra instructions for the LLM.
- `model`: LLM model to use (e.g., "gpt-4.1").
- `provider`: LLM provider ("OpenAI", "AzureOpenAI", "Anthropic", "Gemini", "Ollama").

---

## 6. What Happens When You Run POSTDOC?

- **Code Collection:**  
  POSTDOC collects your code, respecting `.gitignore` and your blacklist.

- **Token Check:**  
  It checks if your code fits within the selected model's context window.

- **Documentation Generation:**  
  For each selected doc type, POSTDOC generates or updates the documentation using your chosen LLM provider.

- **Minimal Updates:**  
  If documentation already exists, POSTDOC will only update, proofread, and tweak it—preserving all critical information and avoiding unnecessary rewrites.

- **Output:**  
  Each doc type is saved as a Markdown file in your output directory (e.g., `quickstart_guide.md`).

---

## 7. Supported Documentation Types

- Readme
- API documentation
- Quickstart guide
- Tutorial
- User guide
- Reference

---

## 8. Troubleshooting

- **Dependency issues:**  
  Make sure you have installed [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync`.

- **OpenAI errors:**  
  Ensure your API key is set in `.env` or your environment.

- **Token limit exceeded:**  
  Try excluding more file types or splitting your codebase.

---

## 9. Project Structure

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

## 10. License

This project is licensed under the [MIT License](LICENSE).

---

## 11. Contributing

Contributions are welcome! Please open issues or pull requests.

---

## 12. Contact

For questions or support, please open an issue on GitHub.

---

**Happy documenting!** 🪄

---

**Tip:**  
You can always re-run POSTDOC to update your documentation as your codebase evolves. Existing docs will be minimally and safely updated.

---

**End of Quickstart Guide**