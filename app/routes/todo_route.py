from fastapi import APIRouter


route = APIRouter()


@route.get("/health")
def health_route():
    return {"status": "ok"}
