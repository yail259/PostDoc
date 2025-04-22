# 🚀 POSTDOC CLI Tool — Developer Quickstart Guide 🪄

Welcome to **POSTDOC** — the magical 🧙‍♂️ command-line wizard that conjures high-quality project documentation, powered by OpenAI! Whether you need a beautiful README, laser-sharp API docs, hands-on tutorials, or an instant Quickstart, **POSTDOC** conjures it all, instantly and intelligently. Let's bring your codebase to life! 🌟

---

## 🤔 What is POSTDOC?

POSTDOC is a CLI tool that **analyzes your codebase and generates beautiful, AI-powered documentation**.
- Supports: README, API Docs, Quickstarts, Tutorials, User Guides, References.
- Interactive or config-driven (YAML) setup.
- Save time and wow users — all in just a few keystrokes.

---

## ⚡️ Quick Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourorg/postdoc.git
   cd postdoc
   pip install -r requirements.txt
   ```

2. **Configure your OpenAI API Key**

   Add your key to a `.env` file:
   ```env
   OPENAI_API_KEY=sk-...
   ```

   Or set it in your shell environment:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

---

## ✨ Your First Documentation Spell

### **Method 1: Interactive Mode**

Just run:
```bash
python postdoc.py
```
You'll be guided step-by-step:
- Select your code or directory 📂
- Pick documentation types 📝
- Choose your output folder
- (Optional) Provide custom instructions to guide the AI 🤖

Config saved for next time? Awesome! 🔖

### **Method 2: Use a YAML Config**

Want fast, repeatable docs? Save a config file!

**config.yaml:**
```yaml
code_path: ./src
output_dir: ./docs
doc_types:
  - Readme
  - API documentation
model: gpt-4.1
custom_instructions: |
  Please make the docs especially clear and add callout boxes for warnings.
```

Run POSTDOC with your settings:
```bash
python postdoc.py -c config.yaml
```

---

## 🍰 Output Example

POSTDOC will create beautifully formatted Markdown files — one per doc type you selected:
```
docs/
  readme.md
  api_documentation.md
```
Just commit and share with your team. 🚀

---

## 🛠️ Power Features

- **Multi-language**: Supports Python, JS, TypeScript, Java, C, Go, C#, and more.
- **Token-safe**: Prevents over-large codebases from breaking the AI limits.
- **Interactive magic**: User-friendly prompts (via questionary and rich).
- **Lightning fast**: Uses loading spinners and progress bars so you know it’s alive ⚡️

---

## 🏆 Why POSTDOC?

- **Zero manual editing**: Let AI handle the boring bits!
- **Consistent, high-quality docs**: Every time, for every project.
- **Customizable**: Add your instructions for brand voice or quirky style.
- **Great for onboarding**: New devs, contributors, even PMs will 💖 you!

---

## 🧩 Troubleshooting & Tips

- 🛑 **Error: OpenAI key missing?**  
  Make sure your `.env` or environment export is correct!

- 🛑 **No docs generated?**  
  Be sure to select at least one documentation type when prompted.

- 🛑 **Token limit exceeded?**  
  Try documenting smaller pieces, or cleaning up unnecessary files.

---

## 🤝 Get Involved

Found a bug? Have a feature request?  
Open an [issue](https://github.com/yourorg/postdoc/issues) or send a PR!

---

🚀 **POSTDOC** is your codebase's new best friend — level up your dev workflow, one magical doc at a time!  
**Ready? Run POSTDOC and unleash the wizardry!** 🪄

---

**Happy Documenting!**  
— The POSTDOC Team