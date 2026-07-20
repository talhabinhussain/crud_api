from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.models.task_model import Task, UpdateTask
from app.repository.task_repo import get_id, insert_task, task_delete


def get_task_by_id(id: int, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")
    return task


def create_task(task_data: dict, session: Session):
    task = Task(**task_data)
    created = insert_task(task, session)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": created.id, "title": created.title, "done": created.done},
    )


def update_task(id: int, update_data: UpdateTask, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    patch_data = update_data.model_dump(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(task, key, value)

    updated = insert_task(task, session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"id": updated.id, "title": updated.title, "done": updated.done},
    )


def remove_task(id: int, session: Session):
    task = get_id(id, session)
    if not task:
        raise HTTPException(status_code=404, detail=f"id {id} not found")

    task_delete(task, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
