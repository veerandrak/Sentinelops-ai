# Reference AWS architecture for the portfolio deployment.
# Deliberately disabled by default to avoid surprise cloud charges.
# Production path: ALB -> ECS/Fargate API -> RDS PostgreSQL/pgvector,
# with ECR images, CloudWatch, Secrets Manager and least-privilege IAM.
#
# Enable only after adding an AWS provider, remote state, networking inputs,
# budgets and account-specific security controls.

locals {
  reference_architecture = {
    ingress       = "Application Load Balancer"
    compute       = "ECS Fargate"
    image_registry = "ECR"
    memory_vector = "RDS PostgreSQL + pgvector"
    secrets       = "Secrets Manager"
    telemetry     = "CloudWatch + OpenTelemetry"
  }
}

output "aws_reference_architecture" { value = local.reference_architecture }
