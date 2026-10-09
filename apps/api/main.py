import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .config import settings
from .database import get_db, init_db, engine
from .models import Task
from .schemas import TaskCreate, TaskResponse, TaskListResponse, HealthResponse
from .queue_producer import queue_producer

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("api.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicjalizacja bazy danych...")
    init_db()
    logger.info("API gotowe do przyjmowania żądań na porcie %s", settings.API_PORT)
    yield
    logger.info("Zamykanie API...")


app = FastAPI(
    title="Training App - API Service",
    description="Mikrousługa REST API zarządzająca zadaniami w architekturze mikrousługowej",
    version="1.0.0",
    lifespan=lifespan,
)

# Konfiguracja CORS (umożliwia bezpośrednią komunikację z frontendem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Diagnostics"])
def health_check(db: Session = Depends(get_db)):
    """Liveness & readiness endpoint sprawdzający połączenie z bazą i brokerem."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    redis_status = "ok" if queue_producer.ping() else "unavailable"

    overall_status = "healthy" if db_status == "ok" else "degraded"

    return HealthResponse(
        status=overall_status,
        database=db_status,
        redis=redis_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/ready", tags=["Diagnostics"])
def readiness_check(db: Session = Depends(get_db)):
    """Readiness endpoint zgodny z K8s - zwraca 200 gdy baza działa, 503 w przeciwnym razie."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}",
        )


@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Tworzy nowe zadanie w bazie i zleca je do kolejki asynchronicznej."""
    task = Task(
        title=task_in.title,
        task_type=task_in.task_type,
        payload=task_in.payload,
        status="PENDING",
        progress=0,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # Przekazanie ID zadania do brokera komunikatów
    queued = queue_producer.enqueue_task(task.id)
    if not queued:
        logger.warning("Zadanie %s utworzone w bazie, ale broker kolejki jest niedostępny.", task.id)

    return task


@app.get("/api/tasks", response_model=TaskListResponse, tags=["Tasks"])
def list_tasks(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """Pobiera listę ostatnich zadań posortowaną malejąco po dacie utworzenia."""
    tasks = (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(Task).count()
    return TaskListResponse(total=total, tasks=tasks)


@app.get("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: str, db: Session = Depends(get_db)):
    """Pobiera szczegóły i aktualny postęp wybranego zadania."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zadanie o ID {task_id} nie zostało znalezione",
        )
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Usuwa zadanie z bazy danych."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zadanie o ID {task_id} nie zostało znalezione",
        )
    db.delete(task)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
