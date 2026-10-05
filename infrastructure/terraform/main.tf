terraform {
  required_version = ">= 1.6.0"
}

# Intentionally provider-neutral in the MVP.
# The next milestone adds an AWS deployment module after the application
# evaluation and security boundaries are validated locally.

output "project" {
  value = "sentinelops-ai"
}
