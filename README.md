# 🪄 POSTDOC: The AI Wizard for Developers! 🪄

_Effortlessly conjure high-quality documentation with a sprinkle of AI magic!_

---

Welcome to **POSTDOC** — your open-source, command-line wizard for automagically generating top-notch documentation from your codebase or single files, powered by OpenAI! ✨

> “Why spend your precious time writing docs, when you can summon them in seconds?”

---

## ✨ Why Postdoc?

- **AI-Powered**: Uses OpenAI to write beautifully professional docs.
- **Super Versatile**: Handles entire codebases or single files, any language.
- **Config or Interactive**: Configure with YAML, or answer a few easy, friendly prompts!
- **Gorgeous Output**: Get READMEs, API docs, Tutorials, and more, in Markdown format!
- **Lightning Fast**: Kick back as documentation appears in seconds, thanks to progress bars and all the bells & whistles.
- **Never Lose Magic**: Easily save your settings, re-run with YAML config, or customize for each run.

---

## 🚀 Quickstart

### 1. **Install**

```bash
git clone https://github.com/your-repo/postdoc.git
cd postdoc
pip install -r requirements.txt
```

### 2. **Set up OpenAI API Key**

POSTDOC relies on OpenAI's API.  
Create a `.env` file in the repo root:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

Or export via terminal:

```bash
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### 3. **Run the Wizard!**

#### **Interactive Mode**

```bash
python postdoc.py
```

You'll be prompted step-by-step to:

- Choose your code directory or file
- Select output directory
- Pick which docs you want (README, API docs, Tutorial, and more!)
- Add custom instructions (optional)
- Choose your favorite OpenAI model
- Save these settings for next time!

#### **Config Mode**

Save your settings to `config.yaml` (can be created interactively):

```yaml
code_path: ./my_project
output_dir: ./my_project/docs
doc_types:
  - Readme
  - API documentation
  - Quickstart guide
model: gpt-4.1
custom_instructions: "Add plenty of examples and keep a friendly tone!"
```

Then run:

```bash
python postdoc.py --config config.yaml
```

---

## 🧙‍♂️ What’s in the Spellbook?

- **Readme** — Give your project a compelling introduction.
- **API documentation** — Let AI walk through your functions and endpoints.
- **Quickstart guide** — No more long onboarding docs!
- **Tutorial** — Give users a guided magical experience.
- **User guide / Reference** — All the details, none of the hassle!

---

## 🛠️ Features

- **YAML-powered**: Ready for CI/CD and reproducibility!
- **Token-safe**: Will never overwhelm your selected LLM's context window.
- **Beautiful UI**: Uses [rich](https://github.com/Textualize/rich) for pretty progress and styled logs.
- **Easy Extensibility**: Add new documentation types or customize templates.
- **Supports common languages**: Python, JS, TS, Java, Go, C, C++, C# by default!

---

## 💡 Examples

#### **Generate a README for your project**

```bash
python postdoc.py -c config.yaml
```

_or just run `python postdoc.py` and answer the prompts!_

#### **Supported documentation types**

- [x] Readme
- [x] API documentation
- [x] Quickstart guide
- [x] Tutorial
- [x] User guide
- [x] Reference

Docs are output as Markdown files in your chosen directory.

---

## 🤔 FAQ

#### **What languages are supported?**

Out of the box: `.py`, `.js`, `.ts`, `.java`, `.go`, `.c`, `.cpp`, `.cs`

#### **Can I add my own doc type?**

Absolutely! Just edit the list in `prompt_user()` for instant new options.

#### **Is it safe for private code?**

OpenAI receives your code. Handle secrets and privacy accordingly.

#### **Does it work with huge codebases?**

The tool checks token limits before generation and warns if your code is too large for the model context window.

---

## 🏗️ Under the Hood

- Uses [OpenAI Python client](https://github.com/openai/openai-python)
- [rich](https://github.com/Textualize/rich) for beautiful CLI
- [questionary](https://github.com/tmbo/questionary) for friendly prompts
- [PyYAML](https://pypi.org/project/PyYAML/) for config management
- [dotenv](https://pypi.org/project/python-dotenv/) for secrets

---

## 📜 License & Contributing

POSTDOC is MIT licensed and welcomes contributions!

- Fork, branch, and PR your improvements!
- Bug reports and feature requests are magical, too.

---

## 🧙‍♀️ Summon Your Docs Now!

```bash
python postdoc.py
```

_...and watch your documentation write itself._

---

**Star** this repo if this tool makes your codebase more magical! ⭐️  
Questions? [Open an issue](https://github.com/your-repo/postdoc/issues)

---

<div align="center">

_🪄 POSTDOC — Docs, conjured. Effortlessly._

</div>
