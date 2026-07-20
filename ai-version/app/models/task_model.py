from sqlalchemy import VARCHAR, Column, Identity, Integer
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int | None = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    title: str = Field(sa_column=Column(VARCHAR(225), nullable=False))
    done: bool = Field(default=False)


class CreateTask(SQLModel):
    title: str
    done: bool = False

    model_config = {
        "json_schema_extra": {"examples": [{"title": "coding", "done": False}]}
    }


class UpdateTask(SQLModel):
    title: str | None = None
    done: bool | None = None

    model_config = {
        "json_schema_extra": {"examples": [{"title": "coding", "done": True}]}
    }
