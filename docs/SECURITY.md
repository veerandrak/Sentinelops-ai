# Security model

SentinelOps treats model output and retrieved/tool content as **untrusted input**, never as authorization.

## Boundaries
- Read-only investigation is the default.
- Tools are explicitly allowlisted; the MCP demo exposes only read operations.
- Mutating/destructive actions require human approval.
- Credentials must use environment/secret injection and must never enter prompts or Git.
- Tool outputs require validation before use.
- Production identities should be least-privilege and short-lived.

## Threat model
| Threat | Control |
|---|---|
| Prompt injection in runbooks | retrieved text cannot grant tool permission |
| Excessive agent permissions | read-only tool surface + action gate |
| Secret leakage | no credentials in demo data; secret-store requirement |
| Hallucinated remediation | evidence returned separately; approval required |
| Autonomous destructive change | destructive/mutating classifier blocks silent execution |
| Poisoned tool output | tool output is data, not policy |

## Production hardening
Add workload identity, OPA/Cedar policy, signed audit events, rate limits, network egress controls, dependency/SBOM scanning, and adversarial prompt-injection evaluations before connecting write-capable infrastructure.
