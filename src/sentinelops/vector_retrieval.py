"""Dependency-light vector retrieval for reproducible local demos."""

import hashlib
import math
import re
from pathlib import Path

DIMS = 256


def _vector(text: str) -> list[float]:
    vector = [0.0] * DIMS
    for token in re.findall(r"[a-z0-9_-]+", text.lower()):
        index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % DIMS
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cos(left, right):
    return sum(x * y for x, y in zip(left, right))


def retrieve(query: str, root: str = "knowledge/runbooks", limit: int = 3) -> list[dict]:
    query_vector = _vector(query)
    hits = []
    for path in Path(root).glob("*.md"):
        content = path.read_text(encoding="utf-8")
        score = _cos(query_vector, _vector(content))
        hits.append(
            {
                "source": str(path),
                "score": round(score, 4),
                "content": " ".join(content.split())[:600],
            }
        )
    return sorted(hits, key=lambda item: item["score"], reverse=True)[:limit]
