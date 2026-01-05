variable "aws_region" { type = string }
variable "backend_image" { type = string }
variable "database_url" { type = string }
variable "s3_bucket" { type = string }
variable "s3_endpoint" { type = string }
variable "frontend_bucket" { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string }
variable "db_name" { type = string }
variable "ecs_execution_role_arn" { type = string }
variable "ecs_task_role_arn" { type = string }
variable "cloudfront_price_class" { type = string default = "PriceClass_100" }
variable "secret_name" { type = string }
variable "secret_payload_json" { type = string }
