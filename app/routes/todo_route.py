from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.models.task_model import Task, UpdateTask, CreateTask
from app.repository.task_repo import all_task
from app.services.task_service import get_task_by_id, get_task_stats, remove_task, task_update
from database.task_db import get_sessin

route = APIRouter()


@route.get("/health")
def health_route():
    return {"status": "ok"}


@route.get("/tasks")
def all_tasks_route(session: Session = Depends(get_sessin)):

    result = all_task(session)

    return result


@route.get("/stats")
def stats_route(session: Session = Depends(get_sessin)):
    return get_task_stats(session)


@route.get("/task/{id}")
def task_by_id(id: int, session: Session = Depends(get_sessin)) -> Task:
    return get_task_by_id(id, session)


@route.post("/task")
def create_task(task: CreateTask, session: Session = Depends(get_sessin)):
    # raise HTTPException(status_code=400, detail="this id is already exist")

    task_obj = Task(**task.model_dump())

    session.add(task_obj)
    session.commit()
    session.refresh(task_obj)

    return JSONResponse(status_code=201, content="task is created")


@route.put("/task/{id}")
def update_task(
    id: int, update_task: UpdateTask, session: Session = Depends(get_sessin)
):
    return task_update(id, update_task, session)


@route.delete("/task/delete/{id}")
def delete_task(id: int, session: Session = Depends(get_sessin)):
    return remove_task(id, session)
