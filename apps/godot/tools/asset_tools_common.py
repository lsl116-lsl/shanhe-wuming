"""Shared deterministic helpers for the generated-asset pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_VERSION = "p2.0"
DEFAULT_SEED = 286


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--force", action="store_true")
    return parser


def write_text(relative_path: str, content: str, force: bool) -> Path:
    target = PROJECT_ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        existing = target.read_text(encoding="utf-8")
        if existing == content:
            print(f"[unchanged] {relative_path}")
            return target
        raise FileExistsError(f"{relative_path} exists; pass --force to rebuild it")
    target.write_text(content, encoding="utf-8", newline="\n")
    print(f"[generated] {relative_path}")
    return target


def ensure_output_path(relative_path: str, force: bool) -> Path:
    target = PROJECT_ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        raise FileExistsError(f"{relative_path} exists; pass --force to rebuild it")
    return target


def svg_document(width: int, height: int, body: str, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f"<defs>{defs}</defs>\n"
        f"{body}\n"
        "</svg>\n"
    )
