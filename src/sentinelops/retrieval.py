from pathlib import Path
import re


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_-]+", text.lower()))


def retrieve_runbooks(query: str, root: str = "knowledge/runbooks", limit: int = 3) -> list[str]:
    """Small deterministic retriever for a zero-cost, reproducible MVP."""
    q = _tokens(query)
    scored: list[tuple[int, str]] = []
    for path in Path(root).glob("*.md"):
        text = path.read_text(encoding="utf-8")
        score = len(q & _tokens(text))
        if score:
            excerpt = " ".join(text.split())[:420]
            scored.append((score, f"{path.name}: {excerpt}"))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored[:limit]]
