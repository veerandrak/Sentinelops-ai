"""MCP server exposing intentionally read-only operational tools."""
from mcp.server.fastmcp import FastMCP
from sentinelops.tools import DemoOpsTools

mcp = FastMCP("SentinelOps")
tools = DemoOpsTools()

@mcp.tool()
def get_deployment(service: str) -> str:
    """Read-only: inspect latest deployment evidence."""
    return tools.deployment(service).detail

@mcp.tool()
def get_metrics(service: str) -> str:
    """Read-only: inspect service metric evidence."""
    return tools.metrics(service).detail

@mcp.tool()
def get_logs(service: str) -> str:
    """Read-only: inspect sanitized service log evidence."""
    return tools.logs(service).detail

if __name__ == "__main__":
    mcp.run()
