FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    API_PORT=8000

# Instalacja podstawowych narzędzi systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Utworzenie nieuprzywilejowanego użytkownika ze względów bezpieczeństwa
RUN useradd -u 10001 -m -s /bin/bash appuser

# Kopiowanie zależności i instalacja
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego serwisu API
COPY . /app/apps/api

# Zmiana uprawnień na rzecz nieuprzywilejowanego użytkownika
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
