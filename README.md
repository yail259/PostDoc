```markdown
# POSTDOC

**The 🧙 wizard for effortlessly conjuring high-quality documentation!**

POSTDOC is a CLI tool that generates or updates documentation for your codebase using OpenAI's API. It can create or minimally update documentation such as READMEs, API docs, quickstart guides, and more, while respecting your `.gitignore` and existing documentation.

---

## Features

- **AI-powered documentation:** Uses OpenAI to generate or update documentation.
- **Minimal, safe changes:** If documentation already exists, POSTDOC will only update, proofread, and tweak it, preserving all critical information and avoiding unnecessary rewrites.
- **Interactive or config-driven:** Use a YAML config file or answer interactive prompts.
- **Respects `.gitignore`:** Only includes files not ignored by your `.gitignore`.
- **Customizable:** Choose which file types to skip, what documentation to generate, and add custom instructions for the language model.

---

## Quickstart

### 1. Install Python

POSTDOC requires **Python 3.10+**.  
Check your version:

```sh
python3 --version
```

### 2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

POSTDOC uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for fast, reliable dependency management.

Follow the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### 3. Install dependencies

From your project directory, run:

```sh
uv sync
```

This will install all required dependencies as specified in `pyproject.toml` and `uv.lock`.

### 4. Set up your OpenAI API key

POSTDOC uses the OpenAI API.  
Create a `.env` file in your project root with:

```
OPENAI_API_KEY=sk-...
```

Or set the environment variable in your shell.

### 5. Run POSTDOC

```sh
python3 core/postdoc.py
```

- You can run interactively, or provide a config file:
  ```sh
  python3 core/postdoc.py --config config.yaml
  ```

---

## Usage

When you run POSTDOC, you can:

- Select the code directory or file to document.
- Choose output location for generated docs.
- Exclude file types/extensions you don't want included.
- Select documentation types to generate (README, API docs, etc).
- Optionally provide custom instructions for the language model.
- Choose the OpenAI model to use.
- Save your settings to a config file for future runs.

POSTDOC will:

- Collect your code (respecting `.gitignore` and your blacklist).
- Check token limits for your selected model.
- Generate or update the selected documentation types.
- Save the results in your chosen output directory.

---

## Updating Existing Documentation

If documentation already exists, POSTDOC will:

- Update, proofread, and tweak it, making only minimal, safe changes.
- Preserve all critical information or replace with equivalent, updated information.
- **IMPORTANT:** It will NOT introduce major rewrites or alter content unnecessarily.

---

## Project Structure

```
core/
  postdoc.py      # Main CLI entry point
  crawler.py      # Code collection and .gitignore handling
  llm.py          # OpenAI API and token counting
pyproject.toml    # Project metadata and dependencies
uv.lock           # Locked dependency versions
config.yaml       # (Optional) Saved configuration
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Please open issues or pull requests.

---

## Acknowledgements

- [OpenAI](https://openai.com/)
- [uv](https://docs.astral.sh/uv/)
- [rich](https://github.com/Textualize/rich)
- [questionary](https://github.com/tmbo/questionary)
- [tiktoken](https://github.com/openai/tiktoken)

---

## Troubleshooting

- **Dependency issues:** Make sure you have installed [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync`.
- **OpenAI errors:** Ensure your API key is set in `.env` or your environment.
- **Token limit exceeded:** Try excluding more file types or splitting your codebase.

---

## Contact

For questions or support, please open an issue on GitHub.

```
**Happy documenting!** 🪄
```
```