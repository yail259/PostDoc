# 🚀 POSTDOC Quickstart Guide: Auto-Generate Docs that Wow! 🪄

Welcome to **POSTDOC**—your new documentation superpower!  
POSTDOC is a magical CLI tool that turns your codebase into sparkling docs (READMEs, API docs, Quickstarts, and more!) using the latest OpenAI models.  
Say goodbye to tedious writing and hello to beautifully crafted, developer-focused documentation in minutes! 🥳

---

## ✨ Why POSTDOC?

- **AI-Powered**: Leverages the world's most advanced language models for sharp, accurate docs.
- **Flexible**: Scan any codebase—Python, JS, Go, C/C++, and more!
- **Interactive or Automated**: Use an interactive wizard, or drop in a config file for zero-click magic.
- **.gitignore-Aware**: Respects your .gitignore—no clutter, no secrets leaked!
- **Customizable**: Choose doc types and even pass custom instructions.
- **Fast & Beautiful**: Enjoy gorgeous, color-coded progress and error messages powered by `rich`.

---

## 🏁 Get Up & Running in 3 Minutes

### 1. Prerequisites

- **Python 3.7+**
- An [OpenAI API key](https://platform.openai.com/account/api-keys)
- Basic command-line skills!

Install required packages with pip:

```bash
pip install openai tiktoken questionary rich pathspec pyyaml python-dotenv
```

---

### 2. Grab POSTDOC

Put `postdoc.py` in your project folder, or anywhere that's convenient.

**TIP:** Make it executable for easy CLI use:
```bash
chmod +x postdoc.py
```

---

### 3. Set Your OpenAI API Key

POSTDOC uses the excellent `python-dotenv` to securely load your API key.

```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

---

### 4. Run the Wizard! 🧙

Launch POSTDOC interactively (no config needed!):

```bash
./postdoc.py
```

You'll breeze through a delightful Q&A:
- Where’s your code? (Directory or file)
- Where to save docs?
- What types of docs? (README, API, Quickstart, User Guide, etc.)
- Any custom instructions for the AI?
- Which model to use? (default: gpt-4.1)
- Save your choices for next time? (config.yaml created automatically!)

*POSTDOC* will then:
- Read in your code (skipping files covered by `.gitignore`)
- Generate each type of doc you chose (see live progress!)
- Save docs as clean markdown files in your chosen directory

---

#### Example Output

```bash
$ ./postdoc.py
🪄 POSTDOC: The 🧙 wizard for effortlessly conjuring high-quality documentation!
Collecting code from /my/project...
✔ Documents generated, goodbye!
```

Find your new docs at:
```
/my/project/Readme.md
/my/project/Quickstart_guide.md
/my/project/API_documentation.md
...
```

---

### 5. Use a Config File (Optional 💾)

Want to automate it for CI/CD or no prompts next time?  
POSTDOC can read settings from a YAML config file:

**Save as `config.yaml`:**
```yaml
code_path: ./src
output_dir: ./docs
doc_types:
  - Readme
  - API documentation
  - Quickstart guide
custom_instructions: |
  Please focus on developer onboarding.
model: gpt-4.1
```
Run non-interactively:
```bash
./postdoc.py --config config.yaml
```

---

## 🛠️ Advanced: How it Works (Beneath the Magic)

- **Collects code** from your target directory (or a single file), skipping files by `.gitignore`, and only includes source files of popular languages.
- **Estimates token usage** to ensure prompts fit the model's limits.
- **Asks OpenAI** to generate doc(s) based on your choices and code.
- **Writes** one Markdown file per doc type, e.g. `readme.md`, `user_guide.md`, etc.

---

## 💡 Pro Tips

- Use `.gitignore` to exclude generated/big/sensitive files.
- Choose only the docs you need (reduce tokens, keep things clear).
- Pass **custom instructions** for tone, level of detail, or target audience.
- Works great with Python, JavaScript/TypeScript, Go, Java, C/C++/C#!

---

## 🚨 Troubleshooting

- **Token/Context window exceeded?**  
  If you see an error like `Token Limit Exceeded`, try excluding large files or breaking your codebase into smaller chunks.

- **API errors?**  
  Double-check your `.env` and OpenAI account status.

- **Permission denied?**  
  Try `chmod +x postdoc.py` or run as `python3 postdoc.py`.

---

## 🎉 That’s it—Happy Documenting!

You’re seconds away from the best docs your project ever had.  
Questions? Feature requests? Let’s make documentation delightful, together!

---

**POSTDOC: Documentation, Reimagined.**  
🧙🚀✨