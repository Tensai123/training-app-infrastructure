# Grupa podsieci dla klastra ElastiCache Redis
resource "aws_elasticache_subnet_group" "redis" {
  name       = "${var.project_name}-${var.environment}-redis-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-subnet-group"
  }
}

# Klaster ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project_name}-${var.environment}-redis"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.redis.id]

  tags = {
    Name = "${var.project_name}-${var.environment}-redis"
  }
}

locals {
  redis_endpoint = aws_elasticache_cluster.redis.cache_nodes[0].address
  redis_url      = "redis://${local.redis_endpoint}:6379/0"
}
