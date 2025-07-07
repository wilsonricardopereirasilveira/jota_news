terraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "rds" {
  source = "./modules/rds"

  environment   = var.environment
  db_name       = var.db_name
  db_username   = var.db_username
  db_password   = var.db_password
  subnet_ids    = var.private_subnet_ids
  vpc_id        = var.vpc_id
}

module "sqs" {
  source = "./modules/sqs"
  environment = var.environment
}

module "lambda" {
  source = "./modules/lambda"
  environment   = var.environment
  subnet_ids    = var.private_subnet_ids
  security_group_ids = [module.rds.security_group_id]
  queue_url     = module.sqs.queue_url
  db_secret_arn = module.rds.db_secret_arn
}

module "ecs" {
  source = "./modules/ecs"
  environment = var.environment
  vpc_id      = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  public_subnet_ids  = var.public_subnet_ids
  db_secret_arn = module.rds.db_secret_arn
}

module "api_gateway" {
  source      = "./modules/api_gateway"
  environment = var.environment
  lb_dns      = module.ecs.lb_dns_name
}

output "api_url" {
  value = module.api_gateway.invoke_url
}
