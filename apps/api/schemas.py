from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Tytuł / nazwa zadania")
    task_type: str = Field(default="data_processing", description="Typ zadania: data_processing, report_generation, export")
    payload: Optional[str] = Field(default=None, description="Parametry lub dane wejściowe dla zadania")


class TaskResponse(BaseModel):
    id: str
    title: str
    task_type: str
    payload: Optional[str] = None
    status: str
    progress: int
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    total: int
    tasks: List[TaskResponse]


class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    timestamp: str
