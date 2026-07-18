from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


route = APIRouter()


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


all_tasks: List[Task] = [
    Task(id=1, title="buy milk"),
    Task(id=2, title="buy groceries"),
    Task(id=3, title="do work", done=True),
]


# print(all_tasks[1].model_dump())


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
