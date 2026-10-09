import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime
from .database import Base


def get_utc_now():
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    task_type = Column(String(50), nullable=False, default="general_processing")
    payload = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    progress = Column(Integer, nullable=False, default=0)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "task_type": self.task_type,
            "payload": self.payload,
            "status": self.status,
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
