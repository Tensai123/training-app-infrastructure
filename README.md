# Training App - Microservices Architecture

Przykładowa aplikacja w architekturze mikrousługowej służąca jako obciążenie (workload) do budowania i testowania infrastruktury (Docker, Kubernetes, monitoring, CI/CD).

## Architektura i Serwisy

Aplikacja składa się z 3 niezależnych mikrousług w katalogu `apps/`:

```
apps/
├── api/        # Serwis REST API (Python / FastAPI)
├── worker/     # Serwis asynchronicznego przetwarzania zadań (Python Daemon)
└── frontend/   # Interfejs użytkownika (React / Vite)
```

### 1. `apps/api` (Backend API)
- **Framework**: FastAPI + SQLAlchemy
- **Port domyślny**: `8000`
- **Endpointy**:
  - `GET /health` – status zdrowia (baza danych, Redis)
  - `GET /ready` – gotowość na przyjmowanie ruchu (K8s readiness)
  - `GET /docs` – interaktywna dokumentacja Swagger UI
  - `GET /api/tasks` – pobieranie listy zadań
  - `POST /api/tasks` – tworzenie nowego zadania i przekazanie do kolejki
  - `GET /api/tasks/{task_id}` – szczegóły i postęp zadania
  - `DELETE /api/tasks/{task_id}` – usunięcie zadania
- **Zmienne środowiskowe**:
  - `DATABASE_URL` (domyślnie `sqlite:///./tasks.db` lub np. `postgresql://user:pass@host:5432/dbname`)
  - `REDIS_URL` (domyślnie `redis://localhost:6379/0`)
  - `TASK_QUEUE_NAME` (domyślnie `tasks_queue`)
  - `API_PORT` (domyślnie `8000`)

### 2. `apps/worker` (Background Worker)
- **Rola**: Proces roboczy konsumujący zadania z kolejki Redis (z mechanizmem fallback na bezpośrednie odpytywanie bazy danych, jeśli Redis nie jest skonfigurowany).
- **Cechy**:
  - Symulacja postępu obliczeń (0% -> 100%)
  - Zapisywanie szczegółowego wyniku JSON w bazie
  - Obsługa błędów (wpisanie `fail` w payloadzie symuluje kontrolowaną awarię)
  - Graceful shutdown (`SIGINT` / `SIGTERM`)
- **Zmienne środowiskowe**:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `TASK_QUEUE_NAME`
  - `WORKER_ID`

### 3. `apps/frontend` (Dashboard UI)
- **Framework**: React 18 + Vite
- **Port deweloperski**: `3000`
- **Funkcje**:
  - Wskaźniki zdrowia API, bazy i Redisa w czasie rzeczywistym
  - Formularz zlecenia nowego zadania (wybór typu zadania, parametrów)
  - Tabela zadań z automatycznym odświeżaniem, paskiem postępu i podglądem wyników

---

## Uruchomienie lokalne (Development)

### Backend API:
```bash
cd apps/api
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8000
```

### Worker:
```bash
cd apps/worker
pip install -r requirements.txt
python -m apps.worker.main
```

### Frontend:
```bash
cd apps/frontend
npm install
npm run dev
```
Otwórz przeglądarkę na `http://localhost:3000`.
