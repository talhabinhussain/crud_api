from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.task_model import CreateTask, UpdateTask
from app.repository.task_repo import all_task
from app.services.task_service import (
    create_task,
    get_task_by_id,
    get_task_stats,
    remove_task,
    update_task,
)
from database.db import get_session

route = APIRouter()


@route.get("/health")
def health_route():
    return {"status": "ok"}


@route.get("/tasks")
def all_tasks_route(session: Session = Depends(get_session)):
    return all_task(session)


@route.get("/stats")
def stats_route(session: Session = Depends(get_session)):
    return get_task_stats(session)


@route.get("/task/{id}")
def task_by_id(id: int, session: Session = Depends(get_session)):
    return get_task_by_id(id, session)


@route.post("/task")
def create_task_route(task: CreateTask, session: Session = Depends(get_session)):
    return create_task(task.model_dump(), session)


@route.put("/task/{id}")
def update_task_route(
    id: int, task: UpdateTask, session: Session = Depends(get_session)
):
    return update_task(id, task, session)


@route.delete("/task/{id}")
def delete_task_route(id: int, session: Session = Depends(get_session)):
    return remove_task(id, session)
