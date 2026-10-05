# Project walkthrough

## Request lifecycle
1. FastAPI validates the incident request.
2. LangGraph carries explicit incident state.
3. Read-only tools collect deployment, metrics and log evidence.
4. Retrieval ranks runbook context and preserves source provenance.
5. The reasoning node correlates evidence into a hypothesis.
6. The guardrail classifies the recommended action.
7. Mutating/destructive actions require human approval.
8. Incident memory can persist outcomes for later investigations.
9. Prometheus instrumentation exposes operational measurements.

## Why start deterministic?
A portfolio reviewer should be able to clone the project and run meaningful tests without an LLM subscription. The architecture therefore works without a paid model. A provider adapter can later replace the deterministic reasoning node without changing the authorization boundary.

## What to demo to a recruiter
Run tests, start the API, analyze `checkout-api`, show the three evidence sources and retrieved runbook, then show that the rollback recommendation is marked as requiring approval. Next, show the LangGraph test and MCP read-only tools. This tells a stronger engineering story than a screenshot of a chatbot.
