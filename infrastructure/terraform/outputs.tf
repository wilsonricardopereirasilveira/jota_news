output "rds_endpoint" {
  value = module.rds.endpoint
}

output "queue_url" {
  value = module.sqs.queue_url
}

output "ecs_service_name" {
  value = module.ecs.service_name
}

output "api_gateway_url" {
  value = module.api_gateway.invoke_url
}
