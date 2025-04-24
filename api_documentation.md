# POSTDOC API Documentation

## Overview

**POSTDOC** is a CLI tool for generating and updating documentation for codebases or single files using OpenAI's API and other LLM providers. It supports interactive configuration, YAML-based config files, and respects `.gitignore` patterns when collecting code. The tool is designed to update, proofread, and tweak existing documentation with minimal, safe changes, preserving all critical information.

---

## Installation

**Dependencies:**  
POSTDOC requires Python 3.10+ and several dependencies managed via [uv](https://docs.astral.sh/uv/getting-started/installation/).

**To install all dependencies:**
1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run in your project directory:
   ```sh
   uv sync
   ```

---

## CLI Usage

```sh
python core/postdoc.py [-c CONFIG]