from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.models.task_model import Task, UpdateTask, CreateTask
from database.task_db import get_sessin

route = APIRouter()


@route.get("/health")
def health_route():
    return {"status": "ok"}


@route.get("/tasks")
def all_tasks_route(session: Session = Depends(get_sessin)):

    get_all_task = session.exec(select(Task)).all()

    return get_all_task


@route.get("/task/{id}")
def task_by_id(id: int, session: Session = Depends(get_sessin)) -> Task:
    # for task in all_tasks:
    #     if task.id == id:
    #         return task
    # raise HTTPException(status_code=404, detail=f"id {id} not found")
    pass


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
    get_task = session.get(Task, id)
    if not get_task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    task_data = update_task.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        setattr(get_task, key, value)

    session.add(get_task)
    session.commit()
    session.refresh(get_task)


@route.delete("/task/delete/{id}")
def delete_task(id: int, session: Session = Depends(get_sessin)):
    get_task = session.get(Task, id)
    if not get_task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")
    session.delete(get_task)
    session.commit()
