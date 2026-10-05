# Interview guide

## 30-second pitch
“SentinelOps is an agentic incident-response platform combining DevOps evidence collection, retrieval, stateful orchestration and safety-gated remediation. A request triggers read-only deployment, metrics and log tools, retrieves runbook context, correlates evidence, and proposes a next action. Infrastructure mutations remain behind a human approval boundary. I added automated evaluation, CI, Docker, Kubernetes and Terraform so the repository demonstrates production engineering around AI rather than only prompting.”

## Architecture concepts you should know
**RAG:** retrieves domain knowledge at request time so answers can be grounded in current runbooks instead of model memory.

**Embeddings/vector search:** represents content numerically and ranks semantically similar chunks. The local MVP uses deterministic hashed vectors so anyone can test it without an API key; the interface can be replaced by pgvector/Qdrant + an embedding model.

**LangGraph:** models the investigation as explicit state transitions: collect → retrieve → reason → gate. This makes branching, retries, persistence and human interrupts easier to add than a single giant prompt.

**MCP:** standardizes how AI applications expose/discover tools and resources. MCP is not authorization; permissions remain a conventional security responsibility.

**Human-in-the-loop:** investigation can be autonomous, but changes with blast radius need approval and policy checks.

## Questions to expect
**Why not automatically rollback?** Model reasoning is probabilistic; infrastructure writes have blast radius. Separate recommendation from authorization.

**How would you productionize retrieval?** Chunk/version runbooks, generate embeddings, store in pgvector/Qdrant, apply metadata/tenant filters, rerank results, cite sources, and measure retrieval recall.

**How do you evaluate an agent?** Use labeled incidents to measure retrieval recall, hypothesis correctness, groundedness, unsafe-action rate, tool success, p50/p95 latency, cost, and human acceptance.

**How do you prevent prompt injection?** Never let retrieved text alter authorization, separate instructions from data, allowlist tools, validate arguments/output, enforce policy outside the model, and test adversarial documents.

**What would you add at scale?** Durable Postgres state, OpenTelemetry traces, Prometheus/Grafana, workload identity, real read-only Kubernetes/GitHub adapters, queues, caching, HA, policy-as-code, and model fallbacks.

## Resume bullet
Use only after you can demo/explain it:

> Built SentinelOps AI, an agentic DevOps incident-response portfolio platform using LangGraph orchestration, MCP-style tools, RAG/vector retrieval, persistent incident memory, safety-gated remediation, automated evaluation, CI/CD, Docker, Kubernetes and Terraform.

Never claim production use or percentage improvements unless actually measured.
