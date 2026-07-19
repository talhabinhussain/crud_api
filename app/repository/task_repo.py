from sqlmodel import Session, select

from app.models.task_model import Task


def all_task(session: Session):
    get_all_task = session.exec(select(Task)).all()
    return get_all_task


def get_id(id: int, session: Session):
    task = session.get(Task, id)
    return task


def insert_task(task: Task, session: Session):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def task_delete(task: Task, session: Session):
    session.delete(task)
    session.commit()
