import logging
import redis
from .config import settings

logger = logging.getLogger("api.queue")


class QueueProducer:
    def __init__(self, redis_url: str = settings.REDIS_URL, queue_name: str = settings.TASK_QUEUE_NAME):
        self.redis_url = redis_url
        self.queue_name = queue_name
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = redis.Redis.from_url(self.redis_url, decode_responses=True)
        return self._client

    def enqueue_task(self, task_id: str) -> bool:
        """Wrzuca ID zadania do kolejki Redis."""
        try:
            self.client.rpush(self.queue_name, task_id)
            logger.info("Zadanie %s dodane do kolejki %s", task_id, self.queue_name)
            return True
        except Exception as e:
            logger.warning("Nie udało się przekazać zadania %s do Redisa: %s", task_id, e)
            return False

    def ping(self) -> bool:
        """Sprawdza połączenie z brokerem Redis."""
        try:
            return bool(self.client.ping())
        except Exception:
            return False


queue_producer = QueueProducer()
