from pathlib import Path
from typing import Iterator
import pathspec
from rich.console import Console

console = Console()


def load_gitignore(root: Path):
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return None
    lines = gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def is_ignored(fp: Path, spec, root: Path) -> bool:
    if spec is None:
        return False
    try:
        rel = fp.relative_to(root).as_posix()
    except ValueError:
        return False
    return spec.match_file(rel)


def find_extensions(dir_path: str) -> list[str]:
    """
    Scan dir_path (respecting .gitignore) and return a sorted list
    of all distinct file extensions (using '(no extension)' if none).
    """
    root = Path(dir_path)
    spec = load_gitignore(root)

    # Gather all non-ignored files
    all_files = [
        fp for fp in root.rglob("*") if fp.is_file() and not is_ignored(fp, spec, root)
    ]

    # Extract extensions
    ext_set = {fp.suffix or "(no extension)" for fp in all_files}
    return sorted(ext_set)


def collect_code_chunks(
    dir_path: str, blacklist: list[str]
) -> Iterator[tuple[dict, list[str]]]:
    """Yield (chunk, warning_messages) tuples, skipping .git and respecting .gitignore."""
    root = Path(dir_path)
    spec = load_gitignore(root)

    warnings = []

    for fp in root.rglob("*"):
        # Skip .git folder entirely
        if ".git" in fp.parts:
            continue

        if not fp.is_file() or is_ignored(fp, spec, root):
            continue

        ext = fp.suffix or "(no extension)"
        if blacklist and ext in blacklist:
            warnings.append(f"Skipping {fp} (extension {ext} not allowed)")
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
            yield {"path": str(fp.relative_to(root)), "content": text}, warnings
            warnings.clear()
        except Exception as e:
            warnings.append(f"Could not read {fp}: {e}")
