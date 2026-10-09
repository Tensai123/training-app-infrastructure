# 1. Security Group dla Load Balancera (ALB)
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Zezwala na ruch HTTP z Internetu do ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP z Internetu"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-alb-sg"
  }
}

# 2. Security Group dla Frontendu
resource "aws_security_group" "frontend" {
  name        = "${var.project_name}-${var.environment}-frontend-sg"
  description = "Ruch do frontendu wylacznie z Load Balancera"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Ruch HTTP z ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-frontend-sg"
  }
}

# 3. Security Group dla API
resource "aws_security_group" "api" {
  name        = "${var.project_name}-${var.environment}-api-sg"
  description = "Ruch do API z ALB oraz z Frontendu"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Ruch HTTP do API z ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id, aws_security_group.frontend.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-api-sg"
  }
}

# 4. Security Group dla Workera
resource "aws_security_group" "worker" {
  name        = "${var.project_name}-${var.environment}-worker-sg"
  description = "Worker nie nasluchuje na zadnym porcie z zewnatrz"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-worker-sg"
  }
}

# 5. Security Group dla Bazy Danych RDS (PostgreSQL)
resource "aws_security_group" "db" {
  name        = "${var.project_name}-${var.environment}-db-sg"
  description = "Dostep do bazy danych PostgreSQL tylko z API i Workera"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL z API i Workera"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id, aws_security_group.worker.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-db-sg"
  }
}

# 6. Security Group dla ElastiCache (Redis)
resource "aws_security_group" "redis" {
  name        = "${var.project_name}-${var.environment}-redis-sg"
  description = "Dostep do Redis tylko z API i Workera"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Redis z API i Workera"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id, aws_security_group.worker.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-sg"
  }
}
