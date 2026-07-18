from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from httpx import delete
from pydantic import BaseModel, field_validator


route = APIRouter()


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class UpdateTask(BaseModel):
    # id: int
    title: str
    done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title cannot be blank")
        return cleaned


all_tasks: List[Task] = [
    Task(id=1, title="buy milk"),
    Task(id=2, title="buy groceries"),
    Task(id=3, title="do work", done=True),
]


@route.get("/health")
def health_route():
    return {"status": "ok"}


@route.get("/task")
def all_tasks_route():

    return all_tasks


@route.get("/task/{id}")
def task_by_id(id: int) -> Task:
    for task in all_tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail=f"id {id} not found")


@route.post("/task")
def create_task(new_task: Task):
    for task in all_tasks:
        if task.id == new_task.id:
            raise HTTPException(status_code=400, detail="this id is already exist")

    return JSONResponse(status_code=201, content="task is created")


@route.put("/task/{id}")
def update_task(id: int, update_task: UpdateTask):
    for task in all_tasks:
        if task.id == id:
            task.title = update_task.title
            task.done = update_task.done
            return JSONResponse(status_code=200, content="updated successfully")

    raise HTTPException(status_code=404, detail=f"id {id} not found")


@route.delete("/task/delete/{id}")
def delete_task(id: int):
    for task in all_tasks:
        if task.id == id:
            all_tasks.remove(task)
            return JSONResponse(status_code=200, content="task is deleted")

    raise HTTPException(status_code=404, detail="not found")
