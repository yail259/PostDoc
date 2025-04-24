from pathlib import Path
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


def collect_code(dir_path: str, blacklisted: list[str]) -> str:
    """
    Walks dir_path (respecting .gitignore), skips any files whose
    extension is in `blacklisted`, and returns a single concatenated string
    of all remaining file contents.
    """
    root = Path(dir_path)
    spec = load_gitignore(root)
    code_str = ""

    for fp in root.rglob("*"):
        if not fp.is_file() or is_ignored(fp, spec, root):
            continue
        ext = fp.suffix or "(no extension)"
        if ext in blacklisted:
            console.print(f"[yellow]Skipping {fp}[/yellow]")
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
            code_str += f"\n\n# File: {fp}\n" + text
        except Exception:
            console.log(f"Warning: Could not read file {fp}")

    return code_str
