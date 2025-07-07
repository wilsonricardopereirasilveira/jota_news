variable "environment" { type = string }
variable "queue_url" { type = string }
variable "dlq_arn" { type = string }
variable "subnet_ids" { type = list(string) }
variable "security_group_ids" { type = list(string) }
variable "db_secret_arn" { type = string }
variable "package_file" { type = string default = "lambda.zip" }
variable "handler" { type = string default = "lambda_function.lambda_handler" }
variable "reserved_concurrency" { type = number default = 1 }
