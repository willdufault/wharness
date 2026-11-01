"""Write content to a file, given a repo-relative path."""

from pathlib import Path


def run(args: str) -> str:
    try:
        path, *rest = args.split(maxsplit=1)
        content = rest[0] if rest else ""
        Path(path).write_text(content)
        return f"Wrote {len(content)} chars to {path}"
    except FileNotFoundError:
        return f"Error: file not found: {path or args}"
