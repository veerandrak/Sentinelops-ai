import time
from contextlib import contextmanager

from prometheus_client import Counter, Histogram

INCIDENTS=Counter("sentinelops_incidents_total","Incident investigations",["service"])
LATENCY=Histogram("sentinelops_investigation_seconds","Investigation latency")
TOOL_ERRORS=Counter("sentinelops_tool_errors_total","Tool errors",["tool"])

@contextmanager
def observe_incident(service: str):
    start=time.perf_counter(); INCIDENTS.labels(service=service).inc()
    try: yield
    finally: LATENCY.observe(time.perf_counter()-start)
