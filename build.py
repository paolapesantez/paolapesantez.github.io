#!/usr/bin/env python3
"""
build.py — drive Quarto from Python.

Quarto itself is a CLI (no importable Python API), so this wraps the
`quarto` executable with subprocess. Useful for CI pipelines, pre-render
data pulls, or just running the whole build with `python build.py`.

Usage:
    python build.py render            # build the static site into _site/
    python build.py render --file publications.qmd   # render one page
    python build.py preview           # live-reloading local preview
    python build.py check             # confirm quarto + deps are installed
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()


def find_quarto() -> str:
    """Locate the quarto executable, checking PATH first."""
    exe = shutil.which("quarto")
    if exe:
        return exe
    raise FileNotFoundError(
        "quarto not found on PATH. Install it from https://quarto.org/docs/get-started/ "
        "or set QUARTO_BIN to the executable path."
    )


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_DIR)
    return result.returncode


def cmd_check(quarto: str) -> int:
    code = run([quarto, "--version"])
    try:
        import bibtexparser, matplotlib, jupyter  # noqa: F401
        print("Python deps OK: bibtexparser, matplotlib, jupyter")
    except ImportError as e:
        print(f"Missing Python dependency: {e}. Run: pip install -r requirements.txt")
        return 1
    return code


def cmd_render(quarto: str, file: str | None) -> int:
    cmd = [quarto, "render"]
    if file:
        cmd.append(file)
    code = run(cmd)
    if code == 0 and not file:
        out = PROJECT_DIR / "_site" / "index.html"
        print(f"\nBuilt site: {out}")
    return code


def cmd_preview(quarto: str) -> int:
    return run([quarto, "preview"])


def cmd_publish(quarto: str) -> int:
    # Publishes _site/ to the gh-pages branch of the current git remote.
    return run([quarto, "publish", "gh-pages"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Quarto from Python.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="Verify quarto + Python deps are installed")

    p_render = sub.add_parser("render", help="Build the static site")
    p_render.add_argument("--file", help="Render a single .qmd file instead of the whole project")

    sub.add_parser("preview", help="Start a live-reloading local preview server")
    sub.add_parser("publish", help="Publish _site/ to GitHub Pages")

    args = parser.parse_args()

    try:
        quarto = find_quarto()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    if args.command == "check":
        return cmd_check(quarto)
    if args.command == "render":
        return cmd_render(quarto, args.file)
    if args.command == "preview":
        return cmd_preview(quarto)
    if args.command == "publish":
        return cmd_publish(quarto)

    return 1


if __name__ == "__main__":
    sys.exit(main())
