import os
from contextlib import suppress

__all__ = ["secret"]


def secret(key: str, default: str = None) -> str:
    """Resolve a secret from argument → env var → Colab userdata secrets."""

    from_env = os.environ.get(key)
    if from_env:
        return from_env

    with suppress():
        from google.colab import userdata
        secret = userdata.get(key)
        if secret:
            return secret
        else:
            print("Warning: Colab secret not found:", key)

    if default is not None:
        return default

    raise ValueError(
        f"{key} not found. "
        f"Set {key} as an env‑var / Colab secret, or pass it directly."
    )
