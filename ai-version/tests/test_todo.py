from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from fastapi.testclient import TestClient
from database.db import get_session
from main import app

test_engine = create_engine("sqlite:///./test_task.db")


def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def setup_module():
    SQLModel.metadata.create_all(test_engine)


def teardown_module():
    SQLModel.metadata.drop_all(test_engine)


class TestTaskAPI:
    def setup_method(self):
        with Session(test_engine) as session:
            session.exec(text("DELETE FROM task"))
            session.commit()

    def test_create_task(self):
        response = client.post("/task", json={"title": "test task"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "test task"
        assert data["done"] is False
        assert "id" in data

    def test_get_all_tasks(self):
        client.post("/task", json={"title": "task 1"})
        client.post("/task", json={"title": "task 2"})
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_task_by_id(self):
        create_resp = client.post("/task", json={"title": "find me"})
        task_id = create_resp.json()["id"]

        response = client.get(f"/task/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "find me"

    def test_get_task_not_found(self):
        response = client.get("/task/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_task(self):
        create_resp = client.post("/task", json={"title": "old title"})
        task_id = create_resp.json()["id"]

        response = client.put(
            f"/task/{task_id}", json={"title": "new title", "done": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "new title"
        assert data["done"] is True

    def test_update_task_not_found(self):
        response = client.put("/task/999", json={"title": "ghost"})
        assert response.status_code == 404

    def test_delete_task(self):
        create_resp = client.post("/task", json={"title": "delete me"})
        task_id = create_resp.json()["id"]

        response = client.delete(f"/task/{task_id}")
        assert response.status_code == 204

        get_response = client.get(f"/task/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self):
        response = client.delete("/task/999")
        assert response.status_code == 404

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
