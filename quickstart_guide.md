# 🚀 Quickstart Guide: POSTDOC 🪄

Welcome to **POSTDOC** — your magic wand for effortlessly conjuring high-quality documentation for any codebase! ✨🧙‍♂️  
Whether you want a snappy Quickstart, a reference manual, or the perfect README, POSTDOC automates it in just a few commands using the power of OpenAI.  
Let’s get you generating documentation that wows your users and teammates! 🚀

---

## 🛠️ What is POSTDOC?

**POSTDOC** is a CLI tool that analyzes your codebase (single files or full projects), then generates developer documentation — such as Readmes, API docs, Quickstarts, and more — using OpenAI models.  
It’s interactive, flexible, and respects your `.gitignore` to avoid documenting unwanted files.  
All you need to provide is your code and (optionally) a YAML config. POSTDOC takes care of the rest!  
Perfect for maintainers, open-source contributors, or anyone who’s tired of manual docs. 🤖

---

## ⚡️ TL;DR — Get Started in 3 Steps

### 1. Install dependencies

Make sure you’ve installed the required Python libraries:

```bash
uv sync
```

---

### 2. Set your OpenAI API Key

POSTDOC relies on OpenAI’s API. You need to [get your API key here](https://platform.openai.com/api-keys).

Save your API key as an environment variable. The easiest way:

```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

> POSTDOC loads `.env` automatically, so you’re good to go!

---

### 3. Run POSTDOC and Follow the Prompts

```bash
python postdoc.py
```

- POSTDOC will interactively ask:
  - Where’s your code (file or directory)?
  - Where to save the docs?
  - Which docs do you want (README, API doc, Quickstart, Tutorial, etc.)?
  - Any special instructions for the AI?
  - Which OpenAI model to use (default: gpt-4.1)?
  - Want to save these settings to `config.yaml` for next time?

---

## 🤩 Example: Let’s Generate a Quickstart!

Suppose your code is in `./myproject`:

```bash
python postdoc.py
```

<details>
<summary>Example Interactive Session</summary>

```txt
Enter the path to the code directory or file:
> ./myproject

Save documentation in the same directory as source? [Y/n]
> Y

Select the types of documentation to generate:
[ ] Readme
[x] Quickstart guide
[ ] API documentation
[ ] Tutorial
> <press Enter>

Enter any custom instructions for the language model (optional):
> Please focus on examples and clarity.

Select the model to use:
> gpt-4.1

Save current settings to config.yaml? [Y/n]
> Y
```

</details>

POSTDOC will:

- 🤖 Collect your code (skipping .gitignored files)
- 🧙‍♂️ Call OpenAI to generate a tailored Quickstart
- 📄 Save `quickstart_guide.md` in your chosen directory
- 🎉 DONE!

---

## 🎛️ Advanced: Using a Config File

You can prefill settings with a `config.yaml`:

```yaml
code_path: ./myproject
output_dir: ./myproject/docs
doc_types:
  - Quickstart guide
  - API documentation
custom_instructions: Write in a playful, inspiring style.
model: gpt-4.1
```

Then just:

```bash
python postdoc.py --config config.yaml
```

---

## ⭐️ Pro Tips

- **.gitignore Support:** Only the files you care about are included.
- **Custom Instructions:** “Explain for juniors”, “Write like a seasoned maintainer”, etc.
- **Choose your Docs:** Generate as many doc types as you want — in one go!
- **Reusable Config:** Save/load settings with `config.yaml`.
- **Handles Big Projects:** Will warn if you hit token limits.
- **Modern Output:** Uses [rich](https://github.com/Textualize/rich) for beautiful CLI feedback.

---

## 🔥 Why Use POSTDOC?

- **Save HOURS** of work every time you start or update a project.
- **Consistent, accurate, up-to-date** documentation.
- **Maintain & share** your code like a PRO.
- **Wow your contributors, users, and your future self!**

---

## 🧙‍♂️ Now Go Create Docs Like Magic!

Ready to revolutionize your documentation workflow?  
**Run `python postdoc.py` now and let POSTDOC conjure your docs!**

---

## 🆘 Need Help?

If you hit issues:

- Check your `OPENAI_API_KEY`
- Ensure your dependencies are installed
- See CLI errors for hints

Questions or features requests? Open an issue or PR — we ❤️ contributions!

---

Happy documenting! ✨📚  
— **POSTDOC Team**

---

**P.S.** If you love POSTDOC, star the repo and share with your friends!  
Documentation shouldn’t be hard — let’s make it magical. 🪄
