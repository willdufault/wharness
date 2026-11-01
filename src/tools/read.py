"""Read the contents of a file, given a repo-relative path."""

from pathlib import Path


def run(args: str) -> str:
    try:
        return Path(args).read_text()
    except FileNotFoundError:
        return f"Error: file not found: {args}"
