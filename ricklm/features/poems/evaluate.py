"""Evaluation module: run poem generation tasks, persist results, and push to GitHub."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from ricklm.features.poems.task import Poem
from ricklm.shared.models.capabilities import GeneratesText


PROMPTS_DIR = "prompts/poems"
EVALUATIONS_DIR = "evaluations"

__all__ = ["evaluate", "evaluate_all", "single", "all", "available_prompts"]

# -- Prompt loading -----------------------------------------------------------

_POEM_KEY_MAP: dict[str, str] = {
    "style": "style",
    "context": "knowing",
    "title": "titled",
    "examples": "eg",
}


def _load_prompt(root: Path, name: str) -> dict:
    """Load a prompt JSON and map its keys to :class:`Poem` constructor kwargs."""
    filepath = root / PROMPTS_DIR / f"{name}.json"
    with open(filepath, encoding="utf-8") as fh:
        data = json.load(fh)
    return {_POEM_KEY_MAP.get(k, k): v for k, v in data.items()}


def available_prompts(root: Path) -> list[str]:
    """Return sorted prompt names found in ``prompts/poems/*.json``."""
    return sorted(f.stem for f in (root / PROMPTS_DIR).glob("*.json"))


# -- Evaluation ---------------------------------------------------------------

def _model_label(model: GeneratesText) -> str:
    return type(model).__name__


def evaluate(
    model: GeneratesText,
    requested: str,
    *,
    times: int = 3,
    root: Path,
) -> Path:
    """Generate poems and write them to ``evaluations/<requested>/<model>/<i>.txt``.

    Returns the output directory.
    """
    params = _load_prompt(root, requested)
    model_name = _model_label(model)

    output_dir = root / EVALUATIONS_DIR / requested / model_name
    output_dir.mkdir(parents=True, exist_ok=True)

    poem = Poem(by=model, **params)
    with poem:
        for i in range(1, times + 1):
            result = str(poem)
            
            filepath = output_dir / f"{i}.txt"
            filepath.write_text(result, encoding="utf-8")

            print(f"  [{requested}] Saved {filepath.relative_to(root)}")

        prompt_path = output_dir / f"prompt.txt"
        prompt_path.write_text(poem.prompt, encoding="utf-8")
        print(f"  [{requested}] Saved prompt to {prompt_path.relative_to(root)}")

    return output_dir


def evaluate_all(
    model: GeneratesText,
    *,
    times: int = 3,
    root: Path,
) -> None:
    """Evaluate every prompt found in ``prompts/poems/``."""
    for name in available_prompts(root):
        print(f"\n{'=' * 40}")
        print(f"  Evaluating: {name}")
        print(f"{'=' * 40}")
        evaluate(model, name, times=times, root=root)


single = evaluate
all = evaluate_all