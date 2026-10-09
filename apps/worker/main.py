import logging
import signal
import sys
import time
import redis

from .config import settings
from .database import get_db_session
from .models import Task
from .tasks import execute_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [worker] %(message)s"
)
logger = logging.getLogger("worker.main")

running = True


def handle_exit_signal(signum, frame):
    global running
    logger.info("Otrzymano sygnał zakończenia (%s). Trwa zamykanie workera...", signum)
    running = False


# Rejestracja obsługi sygnałów systemowych (np. przy zamykaniu w Kubernetes / Docker)
signal.signal(signal.SIGINT, handle_exit_signal)
signal.signal(signal.SIGTERM, handle_exit_signal)


def get_redis_client():
    try:
        client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        client.ping()
        return client
    except Exception as e:
        logger.warning("Brak bezpośredniego połączenia z Redis (%s). Uruchamiam tryb awaryjnego odpytywania bazy (DB polling).", e)
        return None


def fetch_pending_task_from_db():
    """Fallback: pobiera najstarsze oczekujące zadanie bezpośrednio z bazy, gdy Redis nie jest aktywny."""
    session = get_db_session()
    try:
        task = session.query(Task).filter(Task.status == "PENDING").order_by(Task.created_at.asc()).first()
        if task:
            return task.id
        return None
    finally:
        session.close()


def main():
    logger.info("Uruchamianie Workera ID: %s", settings.WORKER_ID)
    redis_client = get_redis_client()

    while running:
        task_id = None

        # 1. Próba pobrania zadania z kolejki Redis (BRPOP)
        if redis_client:
            try:
                item = redis_client.blpop(settings.TASK_QUEUE_NAME, timeout=int(settings.POLL_INTERVAL))
                if item:
                    _, task_id = item
            except Exception as e:
                logger.warning("Błąd komunikacji z Redisem: %s. Przełączam na próbę ponownego połączenia...", e)
                redis_client = None

        # 2. Jeśli brak Redisa, sprawdzamy zadania bezpośrednio w bazie danych
        if not redis_client and running:
            task_id = fetch_pending_task_from_db()
            if not task_id:
                time.sleep(settings.POLL_INTERVAL)
                # Próba re-koneksji do Redisa
                redis_client = get_redis_client()

        # 3. Jeśli mamy zadanie do wykonania
        if task_id and running:
            session = get_db_session()
            try:
                execute_task(session, task_id)
            finally:
                session.close()

    logger.info("Worker %s został pomyślnie zatrzymany.", settings.WORKER_ID)
    sys.exit(0)


if __name__ == "__main__":
    main()
