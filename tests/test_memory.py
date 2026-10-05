from sentinelops.memory import IncidentMemory

def test_incident_memory_roundtrip(tmp_path):
    mem=IncidentMemory(str(tmp_path/"memory.db"))
    mem.remember("checkout-api","rollback proposed",[{"source":"logs"}])
    rows=mem.recent("checkout-api")
    assert rows[0]["summary"]=="rollback proposed"
