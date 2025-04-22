# 🪄 POSTDOC: The Documentation Wizard for Developers! 🪄

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)](https://www.python.org/)  
[![OpenAI Powered](https://img.shields.io/badge/AI-OpenAI-informational)](https://openai.com/)

---

## TL;DR

**POSTDOC** is your magical assistant for conjuring high-quality developer docs—supercharged by OpenAI!  
🏗️ Generate **Readmes, API docs, quickstarts, tutorials**, and more for your codebase in seconds.  
⚡ Smartly respects your `.gitignore`, supports custom instructions, and fits everything in the right model context window—all from your terminal!

> **Let POSTDOC wave its wand over your source code and save hours of soul-crushing documentation writing!**

---

## ✨ Features

- **One Command to Rule Them All**: Write beautiful documentation for any codebase or file in seconds ⚡
- **CLI or Interactive Wizard**: Use config files or let the prompt walk you through settings 🗂️🧙‍♂️
- **Model Powered**: Leverage OpenAI's latest models (fleet support for future models too!) 🤖
- **Smart Code Collection**: Recursively gathers code, skipping files in your `.gitignore` 🦾
- **Multiple Doc Types**: Generate Readme(s), User Guides, Tutorials, Quickstarts, API Docs, and more—together or separately 🧩
- **Custom Instructions**: Enter your own prompts or context for completely tailored docs 📝
- **Saves Your Preferences**: Store and reuse configs via simple YAML 🚀
- **Gorgeous Terminal UX**: Enjoy polished, colorful output thanks to [rich](https://github.com/Textualize/rich) and [questionary](https://github.com/tmbo/questionary) 🌈

---

## 🏁 Quickstart

### 1. Install the Requirements

If you don't have uv installed, install it here https://docs.astral.sh/uv/guides/install-python/.

```bash
# (We recommend using a virtualenv!)
uv sync
```

---

### 2. Add Your OpenAI Key

Create a `.env` file in your project directory with:

```env
OPENAI_API_KEY=sk-YourOpenAIKeyHere
```

Or set it in your shell:

```bash
export OPENAI_API_KEY=sk-YourOpenAIKeyHere
```

---

### 3. Run POSTDOC

#### 📚 Option A: Let the Wizard Guide You (Recommended!)

```bash
python postdoc.py
```

You'll be prompted for:

- The code path (directory or file)
- Where to save the docs
- What type(s) of docs you want (multi-select!)
- Custom instructions (optional)
- Model choice
- Option to save your settings as a YAML config

#### ⚙️ Option B: Use a Config File

Create a `config.yaml` like so:

```yaml
code_path: ./src
output_dir: ./docs
doc_types:
  - Readme
  - API documentation
  - Quickstart guide
custom_instructions: >
  Add a friendly, motivational tone. Include emoji in section headings!
model: gpt-4.1
```

Then run:

```bash
python postdoc.py --config config.yaml
```

---

## 📂 Example Output

- `docs/readme.md`
- `docs/api_documentation.md`
- `docs/quickstart_guide.md`
- etc.

(All files in Markdown, ready to share with your team or publish online!)

---

## 🔍 How It Works

1. **User Chooses or Loads Settings**  
   🛠️ From config file or friendly TUI wizard

2. **POSTDOC Reads Your Codebase**  
   📁 Recursively collects code (respects .gitignore!).

3. **Prompts OpenAI to Generate Documentation**  
   🪄 Supplies code and context to AI, fitting within context limits

4. **Generates & Saves Beautiful Markdown Docs**  
   💾 For each selected document type

---

## 💡 Pro Tips

- Combine multiple doc types in one run!
- Add special instructions like "Add diagrams" or "Focus on the data model"
- Store different config files for different projects or audiences
- Your codebase too big for the context window? Refine `.gitignore` to slim it down

---

## 🛠️ Extending & Customization

POSTDOC is just Python!

- **Add support for new doc types**
- **Swap in new OpenAI models as they appear**
- **Tweak Collection Logic to include/exclude more filetypes**

Contributions & PRs welcome! 🚀

---

## 📎 Requirements

- Python 3.8+
- [openai](https://github.com/openai/openai-python)
- [tiktoken](https://github.com/openai/tiktoken)
- [questionary](https://github.com/tmbo/questionary)
- [rich](https://github.com/Textualize/rich)
- [pathspec](https://github.com/cpburnz/python-path-specification)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [pyyaml](https://github.com/yaml/pyyaml)

---

## 🛡️ License

MIT

---

## 🧙‍♂️ Make Documentation Magical—Let POSTDOC Work for You! 🪄

Questions? Issues?  
Open an issue or PR—POSTDOC welcomes all contributors!

---

Made with 💜 by the POSTDOC community.

---

<!--
Feel free to add badges, screenshots, gifs, etc. for extra sparkle!
-->
