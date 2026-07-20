from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.models.task_model import CreateTask, UpdateTask, Task
from app.repository.task_repo import get_id, get_stats, insert_task, task_delete


# def get_id(id:int):


def get_task_by_id(id: int, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    return task


def create_task(task: CreateTask, session: Session):
    try:
        task_obj = Task(**task.model_dump())
        task_data = insert_task(task_obj, session)
        return task_data
    except Exception as exe:
        raise HTTPException(status_code=500, detail=f"failed to create user {exe}")


def task_update(id: int, update_task: UpdateTask, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    task_data = update_task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    result = insert_task(task, session)

    return JSONResponse(
        status_code=201, content=f"id {result.id} was added successfully"
    )


def get_task_stats(session: Session):
    return get_stats(session)


def remove_task(id: int, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    task_delete(task, session)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content=f"id {id} is deleted"
    )


# get_task = session.get(Task, id)
#     if not get_task:
#         raise HTTPException(status_code=404, detail=f"id {id} not found")

#     task_data = update_task.model_dump(exclude_unset=True)

#     for key, value in task_data.items():
#         setattr(get_task, key, value)

#     session.add(get_task)
#     session.commit()
#     session.refresh(get_task)
