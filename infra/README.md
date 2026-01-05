# Infrastructure

- Terraform in `infra/terraform` provisions AWS VPC, subnets, ALB, ECS Fargate service for backend, S3 bucket, and RDS PostgreSQL.
- Frontend built as static assets to S3 + CloudFront (add distribution + bucket policy in Terraform as needed).
- Secrets managed via AWS SSM Parameter Store/Secrets Manager (wire into ECS task definition env).
- Backups: RDS automated snapshots + S3 versioning and lifecycle policies.
- Scaling: ECS desired count and ALB target tracking; RDS instance class adjustable; add ElastiCache if needed.

## Deploy
```
cd infra/terraform
terraform init
terraform apply -var="aws_region=us-east-1" -var="backend_image=ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/research:latest" -var="database_url=postgresql+psycopg2://..." -var="s3_bucket=research-docs" -var="s3_endpoint=https://s3.amazonaws.com" -var="db_username=app" -var="db_password=secret" -var="db_name=research" -var="ecs_execution_role_arn=..." -var="ecs_task_role_arn=..."
```

## CI/CD
- GitHub Actions CI at `.github/workflows/ci.yml` builds backend/frontend.
- Extend with CD job to push images to ECR and run `terraform apply` or trigger deployment pipeline.
