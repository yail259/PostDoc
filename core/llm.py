from openai import OpenAI
import tiktoken

from dotenv import load_dotenv

import re

# Load environment variables and initialize OpenAI client
load_dotenv()

# Supported models and their context window sizes
models = {"gpt-4.1": {"context_window": 1047576}}

client = OpenAI()

_CODE_FENCE_RE = re.compile(
    r"^\s*```(?:markdown)?[ \t]*\n"  # opening fence, optionally “markdown”
    r"([\s\S]*?)"  # capture everything (including newlines)
    r"\n```[ \t]*\s*$",  # closing fence
    re.MULTILINE,
)


def unwrap_markdown_block(text: str) -> str:
    """
    If `text` is wrapped in a ```markdown … ``` fence, strip the top and bottom fences
    and return the inner content. Otherwise return `text` unchanged.
    """
    m = _CODE_FENCE_RE.match(text)
    if m:
        return m.group(1)
    return text


def check_context_window(model: str, instruct: str, prompt: str):
    """
    Count tokens and return (token_count, context_window, fallback_encoding).
    Does NOT print or exit.
    Raises KeyError if `model` isn’t in `models`.
    """
    context_window = models[model]["context_window"]

    try:
        encoding = tiktoken.encoding_for_model(model)
        fallback = None
    except Exception:
        # fallback to a known encoding
        fallback = "o200k_base"
        encoding = tiktoken.get_encoding(fallback)

    full_prompt = instruct + "\n" + prompt
    token_count = len(encoding.encode(full_prompt, disallowed_special=()))

    return token_count, context_window, fallback


def generate_docs(model: str, instruct: str, prompt: str) -> str:
    """Use OpenAI's API to generate documentation of the specified type."""
    response = client.responses.create(
        model=model,
        instructions=instruct,
        input=prompt,
        temperature=0,
    )
    return unwrap_markdown_block(response.output_text)
