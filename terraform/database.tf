# Generowanie bezpiecznego losowego hasła, jeśli nie zostało podane w zmiennych
resource "random_password" "db_password" {
  length  = 16
  special = false
}

locals {
  db_password = var.db_password != "" ? var.db_password : random_password.db_password.result
}

# Grupa podsieci dla bazy danych w podsieciach prywatnych
resource "aws_db_subnet_group" "db" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-${var.environment}-db-subnet-group"
  }
}

# Instancja bazy danych PostgreSQL (RDS)
resource "aws_db_instance" "postgres" {
  identifier        = "${var.project_name}-${var.environment}-postgres"
  engine            = "postgres"
  engine_version    = "16"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = local.db_password

  db_subnet_group_name   = aws_db_subnet_group.db.name
  vpc_security_group_ids = [aws_security_group.db.id]

  publicly_accessible = false
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name = "${var.project_name}-${var.environment}-postgres"
  }
}

locals {
  database_url = "postgresql://${var.db_username}:${local.db_password}@${aws_db_instance.postgres.endpoint}/${var.db_name}"
}
