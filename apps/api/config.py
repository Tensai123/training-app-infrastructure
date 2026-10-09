import os

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    TASK_QUEUE_NAME: str = os.getenv("TASK_QUEUE_NAME", "tasks_queue")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "*").split(",")
        if origin.strip()
    ]

settings = Config()
