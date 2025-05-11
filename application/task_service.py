import json
from app.domain.models.task_model import TaskCreate, TaskOut
from app.infrastructure.repositories.task_repo import TaskORM, TaskRepository
from fastapi import HTTPException

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, task_data: TaskCreate) -> TaskOut:
        task = self.repo.create(task_data)
        return self._to_task_out(task)

    def get_all_tasks(self) -> list[TaskOut]:
        tasks = self.repo.get_all()
        return [self._to_task_out(task) for task in tasks]

    def update_task(self, task_id: int, task_data: TaskCreate) -> TaskOut:
        task = self.repo.update(task_id, task_data)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return self._to_task_out(task)

    def delete_task(self, task_id: int) -> bool:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return self.repo.delete(task_id)

    def view_task(self, task_id: int) -> TaskOut:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return self._to_task_out(task)

    def _to_task_out(self, task: TaskORM) -> TaskOut:
        return TaskOut(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            assigned_to=task.assigned_to,
            status=task.status,
            user_id=task.user_id,
            project=task.project,
            repeat=task.repeat,
            attachments=json.loads(task.attachments) if task.attachments else [],
            subtasks=json.loads(task.subtasks) if task.subtasks else []
        )