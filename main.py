from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.todo_route import route as todo_route

app = FastAPI()

app.include_router(todo_route)


@app.get("/")
def hello_api():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
