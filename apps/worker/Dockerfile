FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Utworzenie nieuprzywilejowanego użytkownika
RUN useradd -u 10001 -m -s /bin/bash appuser

# Kopiowanie zależności i instalacja
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego serwisu Workera
COPY . /app/apps/worker

# Zmiana uprawnień
RUN chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "apps.worker.main"]
