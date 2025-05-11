from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.application.task_service import TaskService, TaskRepository
from app.domain.models.task_model import TaskCreate, TaskOut
from app.infrastructure.db.db import get_db
from app.presentation.dependencies import get_current_user

router = APIRouter()

def get_task_service(db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return TaskService(repo)

@router.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, current_user=Depends(get_current_user), service: TaskService = Depends(get_task_service)):
    task.user_id = current_user.id
    return service.create_task(task)

@router.get("/tasks", response_model=List[TaskOut])
def list_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_all_tasks()

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.view_task(task_id)

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.update_task(task_id, task_data)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)
    return {"message": "Task deleted successfully"}

@router.get("/tasks/view/{task_id}", response_model=TaskOut)
def view_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.view_task(task_id)
