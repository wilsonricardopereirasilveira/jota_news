variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "private_subnet_ids" { type = list(string) }
variable "image" { type = string default = "api:latest" }
variable "db_secret_arn" { type = string }
variable "region" { type = string default = "us-east-1" }
