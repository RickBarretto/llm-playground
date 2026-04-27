

def store_to(content: str, root: Path, path: str) -> None:
    path = Path(root) / path
    with path.open("w", encoding="utf-8") as file:
        file.write(content)