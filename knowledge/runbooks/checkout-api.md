# Checkout API incident runbook

## Symptoms
Elevated HTTP 5xx, DB timeout errors, or increased p95 latency following a deployment.

## Investigation
1. Compare error-rate onset with the most recent deployment timestamp.
2. Inspect application logs for DB_TIMEOUT and connection-pool exhaustion.
3. Compare the deployed version with the last known-good version.
4. Validate database health before attributing the incident to the application.

## Remediation
A rollback can be proposed when evidence strongly correlates the regression with a release, but production rollback must require explicit human approval.
