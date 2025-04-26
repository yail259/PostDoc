# Runesmith 🧙

**runesmith** is a CLI tool for generating and updating high-quality documentation for codebases or single files using OpenAI's API and other LLM providers. It supports OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama, and can produce a variety of documentation types such as READMEs, API docs, tutorials, and more.

---

## Features

- **Automatic Documentation**: Generate or update documentation for your codebase with a single command.
- **Multiple LLM Providers**: Supports OpenAI, Azure OpenAI, Anthropic, Gemini, and Ollama (local).
- **Context-Aware**: Respects `.gitignore` and existing documentation, making only minimal, safe changes.
- **Interactive or Config-Driven**: Use an interactive wizard or a YAML config file.
- **Customizable**: Choose doc types, blacklist file extensions, and add custom instructions.
- **Token Safety**: Warns if your codebase exceeds the model's context window.

---

## Quickstart

### 1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

[uv](https://docs.astral.sh/uv/getting-started/installation/) is a fast Python package manager and virtual environment tool.

```bash
# Install uv (see https://docs.astral.sh/uv/getting-started/installation/)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Install runesmith from Source

```bash
git clone https://github.com/yail259/runesmith.git
cd runesmith
uv sync
```

This will create a `.venv` and install all dependencies as specified in `pyproject.toml` and `uv.lock`.

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Run runesmith

```bash
runesmith generate
```

- You will be guided through an interactive wizard to select your LLM provider, model, code path, output directory, and documentation types.
- Optionally, you can save your settings to `config.yaml` for future runs.

---

## Usage

### Generate Documentation (Interactive)

```bash
runesmith generate
```

### Generate Documentation from Config

```bash
runesmith generate --config config.yaml
```

### Example `config.yaml`

```yaml
provider: OpenAI
model: gpt-4o
code_path: ./src
output_dir: ./docs
blacklist: [".env", ".pyc"]
doc_types:
  - Readme
  - API documentation
  - Quickstart guide
custom_instructions: |
  Please focus on developer experience and include usage examples.
```

---

## Supported Providers & Models

- **OpenAI**: gpt-4o, gpt-4-turbo, gpt-4.5, etc.
- **Azure OpenAI**: gpt-4o, gpt-4-turbo, etc.
- **Anthropic**: claude-3.5-haiku, claude-3-opus, etc.
- **Gemini**: gemini-1.5-pro, gemini-2.5-pro, etc.
- **Ollama**: Any local model available via Ollama.

> **Note:** Only OpenAI and Ollama are tested by default. For other providers, ensure you have the correct API keys and environment variables set.

---

## Environment Variables

Set the following environment variables as needed for your provider:

- **OpenAI**: `OPENAI_API_KEY`
- **Azure OpenAI**: `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Gemini**: `GEMINI_API_KEY`
- **Ollama**: (runs locally, no key needed)

You can use a `.env` file in your project root.

---

## How It Works

- **Code Collection**: Scans your codebase, respecting `.gitignore` and skipping blacklisted extensions.
- **Token Counting**: Warns if your codebase exceeds the model's context window.
- **Documentation Generation**: Sends your code and instructions to the selected LLM provider.
- **Safe Updates**: If documentation already exists, runesmith will only make minimal, safe changes.

---

## Contributing

Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/yail259/runesmith).

---

## License

MIT License © 2025 yail259

---

## Acknowledgements

- [uv](https://astral.sh/uv/) for fast Python dependency management.
- [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Questionary](https://github.com/tmbo/questionary), and all other open-source dependencies.

---

## TODOs

- [ ] add generated document to context window???
- [ ] add RAG system for context window issue
- [ ] package into binary?
- [ ] multilanguage support?
- [ ] add loop for futher prompting?

---

**Happy documenting! 🧙‍♂️**

---

> _This README was generated and updated by runesmith itself!_
