import os
import uuid

class WorkerConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    TASK_QUEUE_NAME: str = os.getenv("TASK_QUEUE_NAME", "tasks_queue")
    WORKER_ID: str = os.getenv("WORKER_ID", f"worker-{uuid.uuid4().hex[:6]}")
    POLL_INTERVAL: float = float(os.getenv("POLL_INTERVAL", "2.0"))

settings = WorkerConfig()
