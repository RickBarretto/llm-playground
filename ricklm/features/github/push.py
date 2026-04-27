from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from ricklm.shared.models.capabilities import GeneratesText
from ricklm.features.poems.task import Poem


def push_to_github(
    *,
    token: str | None = None,
    name: str | None = None,
    email: str | None = None,
    repo: str = "RickBarretto/llm-playground",
    branch: str = "main",
    message: str = "Publish generated poems",
    root: Path,
) -> None:
    """Stage ``evaluations/``, commit, and push to *repo* on *branch*."""
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
    print(f"Pushed generated poems to {repo} ({branch})")
