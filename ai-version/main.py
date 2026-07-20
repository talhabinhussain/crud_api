from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.task_route import route as task_route
from database.db import create_db_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


app = FastAPI(title="Crud API AI", lifespan=lifespan)
app.include_router(task_route)


@app.get("/")
def hello_api():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks", "/task/{id}"]}
