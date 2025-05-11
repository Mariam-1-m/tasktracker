from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
import json
from app.domain.models.task_model import TaskCreate
from app.infrastructure.db.db import Base
from app.infrastructure.repositories.user_repo import User



class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    due_date = Column(Date)
    priority = Column(String(20), default="medium")
    assigned_to = Column(String(50))
    status = Column(String(20), default="todo")
    project = Column(String(50))
    repeat = Column(String(20))
    attachments = Column(Text)
    subtasks = Column(Text)
    is_comblete = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    
class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task_data: TaskCreate) -> TaskORM:
        db_task = TaskORM(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            assigned_to=task_data.assigned_to,
            user_id=task_data.user_id,
            repeat=task_data.repeat,
            attachments=json.dumps(task_data.attachments),
            subtasks=json.dumps([sub.dict() for sub in task_data.subtasks])
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_all(self) -> list[TaskORM]:
        return self.db.query(TaskORM).all()

    def get_by_id(self, task_id: int) -> Optional[TaskORM]:
        return self.db.query(TaskORM).filter(TaskORM.id == task_id).first()

    def update(self, task_id: int, task_data: TaskCreate) -> Optional[TaskORM]:
        task = self.get_by_id(task_id)
        if not task:
            return None
        for attr, value in task_data.dict().items():
            if attr in ['attachments', 'subtasks']:
                value = json.dumps(value)
            setattr(task, attr, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True
