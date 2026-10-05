"""Dependency-light semantic-ish vector retrieval for reproducible local demos.

Uses hashed term vectors + cosine similarity. The Retriever interface is deliberately
replaceable by pgvector/Qdrant/managed embeddings in production.
"""
import hashlib
import math
import re
from pathlib import Path

DIMS = 256

def _vector(text: str) -> list[float]:
    v=[0.0]*DIMS
    for token in re.findall(r"[a-z0-9_-]+", text.lower()):
        i=int(hashlib.sha256(token.encode()).hexdigest(),16)%DIMS
        v[i]+=1.0
    norm=math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/norm for x in v]

def _cos(a,b): return sum(x*y for x,y in zip(a,b))

def retrieve(query: str, root: str="knowledge/runbooks", limit: int=3) -> list[dict]:
    q=_vector(query); hits=[]
    for p in Path(root).glob("*.md"):
        text=p.read_text(encoding="utf-8")
        score=_cos(q,_vector(text))
        hits.append({"source":str(p),"score":round(score,4),"content":" ".join(text.split())[:600]})
    return sorted(hits,key=lambda x:x["score"],reverse=True)[:limit]
