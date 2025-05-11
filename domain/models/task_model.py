from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Subtask(BaseModel):
    title: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: str = "medium"
    assigned_to: Optional[str] = None
    status: str = "todo"
    user_id: Optional[int] = None
    project: Optional[str] = None
    repeat: Optional[str] = None
    attachments: List[str] = []
    subtasks: List[Subtask] = []

class TaskOut(TaskCreate):
    id: int