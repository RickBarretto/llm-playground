from pathlib import Path

__all__ = ["store_to"]

def store_to(content: str, file: Path) -> None:
    with file.open("w", encoding="utf-8") as f:
        f.write(content)
