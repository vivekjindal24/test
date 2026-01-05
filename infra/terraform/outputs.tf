output "alb_dns_name" { value = aws_lb.app.dns_name }
output "s3_bucket" { value = aws_s3_bucket.docs.bucket }
output "db_endpoint" { value = aws_db_instance.postgres.endpoint }
output "cloudfront_domain" { value = aws_cloudfront_distribution.spa.domain_name }
output "frontend_bucket" { value = aws_s3_bucket.frontend.bucket }
output "secret_arn" { value = aws_secretsmanager_secret.app.arn }
