import tiktoken

from dotenv import load_dotenv

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

PROVIDER_MODELS = {
    "OpenAI": {
        "gpt-4.1": 1_000_000,
        "gpt-4o": 128_000,
        "gpt-4.5": 128_000,
        "gpt-4-turbo": 128_000,
        # "o4-mini": 200_000, # temperature is not supported
        # "o3": 200_000, # temperature is not supported
    },
    "AzureOpenAI": {
        "gpt-4o": 128_000,
        "gpt-4-turbo": 128_000,
        "gpt-4o-mini": 128_000,
        # "o4-mini": 200_000, # temperature is not supported
        # "o3": 200_000, # temperature is not supported
    },
    "Anthropic": {
        "claude-3.7-sonnet": 200_000,
        "claude-3.5-haiku": 200_000,
        "claude-3-opus": 200_000,
    },
    "Gemini": {
        "gemini-2.5-pro-preview-03-25": 1_000_000,
        "gemini-2.5-flash-preview-04-17": 1_000_000,
        "gemini-2.0-flash": 1_000_000,
        "gemini-1.5-pro": 2_000_000,
    },
}


def unwrap_markdown_block(text: str) -> str:
    """
    If `text` starts with ```markdown and ends with ```, remove the fences
    and return the inner content. Otherwise return the text unchanged.
    """
    lines = text.splitlines()

    if (
        len(lines) >= 2
        and lines[0].strip() == "```markdown"
        and lines[-1].strip() == "```"
    ):
        return "\n".join(lines[1:-1])

    return text


def get_context_window(provider: str, model: str) -> int:
    """
    Lookup context window size for a model.
    Returns inf if unknown.
    """
    try:
        return PROVIDER_MODELS[provider][model]["context_window"]
    except Exception:
        return float("inf")


def count_tokens(text: str, model: str) -> tuple[int, str | None]:
    """
    Count tokens in text for the given model.
    Returns (token_count, fallback_encoding_used).
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        fallback = None
    except Exception:
        fallback = "o200k_base"
        encoding = tiktoken.get_encoding(fallback)

    token_count = len(encoding.encode(text, disallowed_special=()))
    return token_count, fallback


def check_context_window(provider: str, model: str, instruct: str, prompt: str):
    """
    Wrapper: Get token count, context window, and fallback encoding.
    """
    context_window = get_context_window(provider, model)
    full_prompt = instruct + "\n" + prompt
    token_count, fallback = count_tokens(full_prompt, model)
    return token_count, context_window, fallback


def _generate_openai(
    model: str, instruct: str, prompt: str, temperature: float, **kw
) -> str:
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
        temperature=temperature,
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
    google = _lazy_import("google")
    types = google.genai.types
    client = google.genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=instruct,
        ),
    )
    return response.text


def get_ollama_models():
    ollama_sdk = _lazy_import("ollama")
    names = [x.model for x in ollama_sdk.list().models]

    return names


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
