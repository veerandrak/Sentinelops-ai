from dataclasses import dataclass


@dataclass(frozen=True)
class ToolEvidence:
    source: str
    detail: str


class DemoOpsTools:
    """Safe adapters that emulate read-only infrastructure evidence."""

    def deployment(self, service: str) -> ToolEvidence:
        if service == "checkout-api":
            return ToolEvidence("deployment", "v2.4.1 deployed 8 minutes before error-rate increase")
        return ToolEvidence("deployment", f"No recent deployment signal found for {service}")

    def metrics(self, service: str) -> ToolEvidence:
        if service == "checkout-api":
            return ToolEvidence("metrics", "HTTP 5xx rose from baseline to 18%; latency p95 also increased")
        return ToolEvidence("metrics", f"No abnormal demo metric signal found for {service}")

    def logs(self, service: str) -> ToolEvidence:
        if service == "checkout-api":
            return ToolEvidence("logs", "Repeated DB_TIMEOUT errors began after v2.4.1 rollout")
        return ToolEvidence("logs", f"No matching demo error pattern found for {service}")
