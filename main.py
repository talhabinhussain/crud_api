from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes.todo_route import route as todo_route
from database.task_db import create_db_table

app = FastAPI(title="Crud API")

app.include_router(todo_route)


@app.on_event("startup")
def on_startup():
    create_db_table()


@app.get("/")
def hello_api():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
