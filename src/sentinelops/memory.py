import json
import sqlite3
from pathlib import Path

class IncidentMemory:
    """Durable local incident memory. Production can swap this adapter for Postgres."""
    def __init__(self, path: str = "data/sentinelops.db"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY, service TEXT, summary TEXT, evidence TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def _db(self):
        return sqlite3.connect(self.path)

    def remember(self, service: str, summary: str, evidence: list[dict]) -> int:
        with self._db() as db:
            cur = db.execute("INSERT INTO incidents(service,summary,evidence) VALUES(?,?,?)", (service, summary, json.dumps(evidence)))
            return int(cur.lastrowid)

    def recent(self, service: str, limit: int = 5) -> list[dict]:
        with self._db() as db:
            rows = db.execute("SELECT id,summary,evidence,created_at FROM incidents WHERE service=? ORDER BY id DESC LIMIT ?", (service, limit)).fetchall()
        return [{"id": r[0], "summary": r[1], "evidence": json.loads(r[2]), "created_at": r[3]} for r in rows]
