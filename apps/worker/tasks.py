import json
import logging
import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from .models import Task
from .config import settings

logger = logging.getLogger("worker.tasks")


def execute_task(db: Session, task_id: str) -> bool:
    """Wykonuje zadanie, aktualizuje postęp i zapisuje rezultat w bazie danych."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Nie znaleziono zadania o ID %s", task_id)
        return False

    # Sprawdzenie czy zadanie nie zostało już wcześniej obsłużone
    if task.status in ["RUNNING", "COMPLETED"]:
        logger.info("Zadanie %s jest już w stanie %s, pomijam.", task_id, task.status)
        return True

    logger.info("Rozpoczynanie przetwarzania zadania %s (%s)", task.id, task.title)
    task.status = "RUNNING"
    task.progress = 10
    db.commit()

    start_time = time.time()

    try:
        # Symulacja kroków obliczeniowych z raportowaniem postępu
        steps = [25, 50, 75, 95]
        for progress_value in steps:
            time.sleep(1.0)  # Symulacja pracy procesora/I/O
            task.progress = progress_value
            db.commit()
            logger.info("Zadanie %s: postęp %d%%", task.id, progress_value)

            # Testowa symulacja błędu, jeśli w ładunku zadania wpisano "fail"
            if task.payload and "fail" in task.payload.lower():
                raise RuntimeError(f"Wymuszony błąd testowy na etapie {progress_value}% dla ładunku: {task.payload}")

        # Finalizacja zadania
        time.sleep(0.5)
        duration = round(time.time() - start_time, 2)
        result_data = {
            "worker_id": settings.WORKER_ID,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": duration,
            "summary": f"Pomyślnie przetworzono zadanie typu '{task.task_type}'",
            "details": {
                "original_title": task.title,
                "input_payload": task.payload,
            }
        }

        task.progress = 100
        task.status = "COMPLETED"
        task.result = json.dumps(result_data, indent=2, ensure_ascii=False)
        task.error = None
        db.commit()
        logger.info("Zadanie %s zakończone sukcesem w czasie %ss", task.id, duration)
        return True

    except Exception as exc:
        duration = round(time.time() - start_time, 2)
        logger.error("Błąd podczas przetwarzania zadania %s: %s", task.id, exc)
        task.status = "FAILED"
        task.error = str(exc)
        task.result = json.dumps({
            "worker_id": settings.WORKER_ID,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": duration,
        })
        db.commit()
        return False
