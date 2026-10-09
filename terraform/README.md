# AWS ECS Fargate Infrastructure (Terraform)

Kod Terraform do wdrożenia architektury mikrousługowej na platformie **AWS ECS Fargate**.

---

## Architektura infrastruktury

```mermaid
flowchart TD
    User([Użytkownik / Internet]) -->|HTTP :80| ALB[Application Load Balancer]

    subgraph VPC ["VPC (10.0.0.0/16)"]
        subgraph PublicSubnets ["Public Subnets"]
            ALB
            NAT[NAT Gateway]
        end

        subgraph PrivateSubnets ["Private Subnets"]
            FE[ECS Service: Frontend\n:80]
            API[ECS Service: API\n:8000]
            Worker[ECS Service: Worker]
            RDS[(RDS PostgreSQL\n:5432)]
            Redis[(ElastiCache Redis\n:6379)]
        end
    end

    ALB -->|/*| FE
    ALB -->|/api/*, /health, /docs| API
    FE -.->|Proxy /api| API
    API -->|Zapis / Odczyt| RDS
    API -->|Kolejka| Redis
    Worker -->|Pobieranie z kolejki| Redis
    Worker -->|Aktualizacja postępu| RDS
    NAT -.->|Wychodzący ruch (pull obrazów, logi CloudWatch)| PrivateSubnets
```

---

## Wymagania wstępne
1. Zainstalowane narzędzie **Terraform** (`>= 1.5.0`).
2. Skonfigurowane poświadczenia AWS CLI (`aws configure`).
3. Zbudowane i wypchnięte obrazy na Docker Hub (`training-api`, `training-worker`, `training-frontend`).

---

## Instrukcja wdrożenia

### 1. Inicjalizacja:
```bash
cd terraform
terraform init
```

### 2. Przygotowanie zmiennych:
Skopiuj plik przykładowy:
```bash
cp terraform.tfvars.example terraform.tfvars
```
Uzupełnij w `terraform.tfvars` nazwę użytkownika Docker Hub:
```hcl
dockerhub_username = "twoj-login-dockerhub"
aws_region         = "eu-central-1"
```

### 3. Weryfikacja planu zmian:
```bash
terraform plan
```

### 4. Wdrożenie infrastruktury:
```bash
terraform apply
```

Po zakończeniu wdrożenia Terraform wyświetli adres URL w outputach:
```text
application_url = "http://training-app-dev-alb-123456789.eu-central-1.elb.amazonaws.com"
api_swagger_url = "http://training-app-dev-alb-123456789.eu-central-1.elb.amazonaws.com/docs"
```

### 5. Sprzątanie zasobów (zniszczenie infrastruktury):
```bash
terraform destroy
```
