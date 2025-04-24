import tiktoken

from dotenv import load_dotenv

import re

# Optional imports guarded at runtime so that missing libraries only matter
# when their provider is actually used.
from importlib import import_module
import os

from pathlib import Path


def _lazy_import(name: str):
    """Import a module only when needed, raising a friendly error otherwise."""
    try:
        return import_module(name)
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            f"Provider requires the `{name}` package – install it first."
        ) from exc


# Pull in any OPENAI_API_BASE you set in your CLI (or in .env)
load_dotenv()

# Supported models and their context window sizes
models = {
    "gpt-4.1": {"context_window": 1047576},
    "phi4": {"context_window": 16000},
}


_CODE_FENCE_RE = re.compile(
    r"^\s*```(?:markdown)?[ \t]*\n"  # opening fence, optionally “markdown”
    r"([\s\S]*?)"  # capture everything
    r"\n```[ \t]*\s*$",  # closing fence
    re.MULTILINE,
)


def unwrap_markdown_block(text: str) -> str:
    """
    If `text` is wrapped in a ```markdown … ``` fence, strip the fences
    and return the inner content. Otherwise return text unchanged.
    """
    m = _CODE_FENCE_RE.match(text)
    return m.group(1) if m else text


def check_context_window(model: str, instruct: str, prompt: str):
    """
    Count tokens and return (token_count, context_window, fallback_encoding).
    Raises KeyError if `model` isn’t in `models`.
    """
    context_window = models[model]["context_window"]

    try:
        encoding = tiktoken.encoding_for_model(model)
        fallback = None
    except Exception:
        fallback = "o200k_base"
        encoding = tiktoken.get_encoding(fallback)

    full_prompt = instruct + "\n" + prompt
    token_count = len(encoding.encode(full_prompt, disallowed_special=()))

    return token_count, context_window, fallback


def _generate_openai(model: str, instruct: str, prompt: str) -> str:
    """
    Use OpenAI's API to generate documentation.
    Honors any OPENAI_API_BASE you’ve set in your environment.
    """
    openai_sdk = _lazy_import("openai")
    client = openai_sdk.OpenAI()

    response = client.responses.create(
        model=model,
        instructions=instruct,
        input=prompt,
        temperature=0,
    )
    return response.output_text


def _generate_azure(
    model: str, instruct: str, prompt: str, temperature: float, **kw
) -> str:
    openai_sdk = _lazy_import("openai")
    azure_client = openai_sdk.AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )
    resp = azure_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instruct},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content


def _generate_anthropic(
    model: str, instruct: str, prompt: str, temperature: float, **kw
) -> str:
    anthropic_sdk = _lazy_import("anthropic")
    client = anthropic_sdk.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=model,
        system=instruct,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=4096,
    )
    return resp.content[0].text


def _generate_google(
    model: str, instruct: str, prompt: str, temperature: float, **kw
) -> str:
    genai = _lazy_import("google.generativeai")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    gmodel = genai.GenerativeModel(model_name=model)
    resp = gmodel.generate_content(
        [
            {"role": "system", "parts": [instruct]},
            {"role": "user", "parts": [prompt]},
        ],
        generation_config={"temperature": temperature},
    )
    return resp.text


def _generate_ollama(
    model: str, instruct: str, prompt: str, temperature: float, **kw
) -> str:
    openai_sdk = _lazy_import("openai")
    client = openai_sdk.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instruct},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content


_GENERATORS = {
    "openai": _generate_openai,
    "azureopenai": _generate_azure,
    "anthropic": _generate_anthropic,
    "google": _generate_google,
    "ollama": _generate_ollama,
}


def is_within_directory(path: Path, directory: Path) -> bool:
    """
    Returns True if `path` is located somewhere under `directory`.
    """
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def build_instruction(
    doc_type: str, custom_instruct: str, output_dir: str, code_path: str
) -> str:
    """
    Construct the instruction string for generating or updating documentation.

    - If the output file exists and is NOT under `code_path`, its contents
      will be appended to the update prompt.
    - If the file exists under `code_path`, or doesn’t exist at all, it
      will skip reading the file and fall back to the appropriate base prompt.
    """
    out_file = Path(output_dir) / f"{doc_type.lower().replace(' ', '_')}.md"

    if out_file.exists():
        existing_doc = ""
        # only read the existing file if it's NOT inside code_path
        if not is_within_directory(out_file, Path(code_path)):
            existing_doc = out_file.read_text()
        return (
            "The documentation already exists. Update, proofread, and tweak it, making only minimal, safe changes. "
            "Preserve all critical information or replace with equivalent, updated information. "
            "IMPORTANT: do NOT introduce major rewrites or alter content unnecessarily."
            f"{custom_instruct}"
            f"{existing_doc}"
        )
    else:
        return (
            f"You are an expert coder and explainer that writes high-quality {doc_type} for developers. "
            f"{custom_instruct}"
        )


DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()


def generate_docs(
    model: str,
    instruct: str,
    prompt: str,
    *,
    provider: str | None = None,
    temperature: float = 0.0,
) -> str:
    """Route documentation generation to the chosen provider.

    Parameters
    ----------
    model       : Name of the model, e.g. "gpt-4o-mini" or "claude-3-haiku".
    instruct    : System or instructions string.
    prompt      : User prompt / codebase content.
    provider    : Provider key – openai | azureopenai | anthropic | google | ollama.
                Defaults to env var *LLM_PROVIDER* (or "openai").
    temperature : Sampling temperature (default 0 for deterministic output).
    """
    backend = (provider or DEFAULT_PROVIDER).lower()
    if backend not in _GENERATORS:
        raise ValueError(
            f"Unsupported provider '{backend}'. Valid options: {', '.join(_GENERATORS)}"
        )
    raw = _GENERATORS[backend](model, instruct, prompt, temperature=temperature)
    return unwrap_markdown_block(raw)
