output "application_url" {
  description = "Publiczny adres URL aplikacji (Frontend)"
  value       = "http://${aws_lb.main.dns_name}"
}

output "api_swagger_url" {
  description = "Publiczny adres interaktywnej dokumentacji Swagger OpenAPI"
  value       = "http://${aws_lb.main.dns_name}/docs"
}

output "alb_dns_name" {
  description = "Nazwa DNS Load Balancera"
  value       = aws_lb.main.dns_name
}

output "ecs_cluster_name" {
  description = "Nazwa klastra ECS"
  value       = aws_ecs_cluster.main.name
}

output "rds_endpoint" {
  description = "Punkt końcowy bazy danych RDS PostgreSQL"
  value       = aws_db_instance.postgres.endpoint
}

output "redis_endpoint" {
  description = "Punkt końcowy klastra ElastiCache Redis"
  value       = local.redis_endpoint
}
