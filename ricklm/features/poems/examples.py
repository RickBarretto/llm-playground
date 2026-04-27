from pathlib import Path
from typing import Iterable

def examples_at(path: str) -> Iterable[str]:
    samples = "Original"
    for file in (Path(path) / samples).glob("[1-9].txt"):
        yield file.read_text()
