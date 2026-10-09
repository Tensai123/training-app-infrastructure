variable "aws_region" {
  type        = string
  description = "Region AWS, w którym wdrażana jest infrastruktura"
  default     = "eu-central-1"
}

variable "environment" {
  type        = string
  description = "Środowisko wdrożenia (np. dev, staging, prod)"
  default     = "dev"
}

variable "project_name" {
  type        = string
  description = "Nazwa projektu używana jako prefiks zasobów"
  default     = "training-app"
}

variable "dockerhub_username" {
  type        = string
  description = "Nazwa użytkownika na Docker Hub, z którego pobierane są obrazy"
  default     = "tensai123"
}

variable "api_image_tag" {
  type        = string
  description = "Tag obrazu dla serwisu API"
  default     = "latest"
}

variable "worker_image_tag" {
  type        = string
  description = "Tag obrazu dla serwisu Workera"
  default     = "latest"
}

variable "frontend_image_tag" {
  type        = string
  description = "Tag obrazu dla serwisu Frontendu"
  default     = "latest"
}

variable "vpc_cidr" {
  type        = string
  description = "Pula adresowa CIDR dla sieci VPC"
  default     = "10.0.0.0/16"
}

variable "db_name" {
  type        = string
  description = "Nazwa bazy danych PostgreSQL"
  default     = "trainingdb"
}

variable "db_username" {
  type        = string
  description = "Nazwa użytkownika bazy danych PostgreSQL"
  default     = "dbadmin"
}

variable "db_password" {
  type        = string
  description = "Hasło do bazy danych PostgreSQL (jeśli puste, zostanie wygenerowane losowo)"
  default     = ""
  sensitive   = true
}

variable "fargate_cpu" {
  type        = number
  description = "Wielkość CPU dla zadań Fargate (256 = 0.25 vCPU)"
  default     = 256
}

variable "fargate_memory" {
  type        = number
  description = "Wielkość pamięci RAM dla zadań Fargate (512 = 512 MiB)"
  default     = 512
}
