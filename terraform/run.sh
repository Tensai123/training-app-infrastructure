#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "==============================================="
echo "   AWS ECS Fargate - Local Deployment Runner   "
echo "==============================================="

case "$1" in
  plan)
    echo "Sprawdzanie planu wdrożenia (terraform plan)..."
    terraform plan
    ;;
  apply)
    echo "Wdrażanie infrastruktury w AWS (terraform apply)..."
    terraform apply
    ;;
  destroy)
    echo "Usuwanie zasobów w AWS (terraform destroy)..."
    terraform destroy
    ;;
  outputs)
    terraform output
    ;;
  *)
    echo "Użycie: ./run.sh [plan|apply|destroy|outputs]"
    echo ""
    echo "Przykłady:"
    echo "  ./run.sh plan     - Wyświetla planowane zmiany bez wdrażania"
    echo "  ./run.sh apply    - Wdraża całą infrastrukturę w AWS"
    echo "  ./run.sh outputs  - Pokazuje adresy URL po wdrożeniu"
    echo "  ./run.sh destroy  - Kasuje wszystkie utworzone zasoby w AWS"
    exit 1
    ;;
esac
