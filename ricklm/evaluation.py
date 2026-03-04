"""Evaluation module: run poem generation tasks, persist results, and push to GitHub."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from ricklm.models.capabilities import GeneratesText
from ricklm.tasks.poem import Poem


PROMPTS_DIR = "prompts/poems"
EVALUATIONS_DIR = "evaluations"


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
    iterations: int = 3,
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
        for i in range(1, iterations + 1):
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
    iterations: int = 3,
    root: Path,
) -> None:
    """Evaluate every prompt found in ``prompts/poems/``."""
    for name in available_prompts(root):
        print(f"\n{'=' * 40}")
        print(f"  Evaluating: {name}")
        print(f"{'=' * 40}")
        evaluate(model, name, iterations=iterations, root=root)


# -- GitHub push --------------------------------------------------------------

def _resolve_secret(value: str | None, key: str) -> str:
    """Resolve a secret from argument → env var → Colab userdata secrets."""
    if value:
        return value

    from_env = os.environ.get(key)
    if from_env:
        return from_env

    try:                                       # Colab userdata secrets
        from google.colab import userdata      # type: ignore[import-untyped]
        secret = userdata.get(key)
        if secret:
            return secret
    except Exception:
        pass

    raise ValueError(
        f"{key} not found. "
        f"Set {key} as an env‑var / Colab secret, or pass it directly."
    )


def push_to_github(
    *,
    token: str | None = None,
    name: str | None = None,
    email: str | None = None,
    repo: str = "RickBarretto/llm-playground",
    branch: str = "main",
    message: str = "Add evaluation results",
    root: Path,
) -> None:
    """Stage ``evaluations/``, commit, and push to *repo* on *branch*."""
    token = _resolve_secret(token, "GITHUB_TOKEN")
    name = _resolve_secret(name, "GIT_NAME")
    email = _resolve_secret(email, "GIT_EMAIL")
    cwd = str(root)
    remote = f"https://x-access-token:{token}@github.com/{repo}.git"

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=cwd,
            check=True, capture_output=True, text=True,
        )

    # Ensure we are inside the cloned repo
    if not (root / ".git").exists():
        raise RuntimeError(
            f"{root} is not a git repository. "
            "Make sure the repo was cloned first."
        )

    # Colab has no git identity by default
    git("config", "user.email", email)
    git("config", "user.name", name)

    git("remote", "set-url", "origin", remote)
    git("add", "evaluations/")

    # Anything staged?
    diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=cwd, capture_output=True,
    )
    if diff.returncode == 0:
        print("No new evaluation files to commit.")
        return

    git("commit", "-m", message)
    git("push", "origin", branch)
    print(f"Pushed evaluation results to {repo} ({branch})")
