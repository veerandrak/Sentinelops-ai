from sentinelops.memory import IncidentMemory


def test_incident_memory_roundtrip(tmp_path):
    memory = IncidentMemory(str(tmp_path / "memory.db"))
    memory.remember("checkout-api", "rollback proposed", [{"source": "logs"}])
    rows = memory.recent("checkout-api")
    assert rows[0]["summary"] == "rollback proposed"
