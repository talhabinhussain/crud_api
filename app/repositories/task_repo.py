from sqlmodel import Session, func, select

from app.models.task_model import Task


def all_task(session: Session, search: str | None = None, done: bool | None = None):
    query = select(Task)

    if search:
        query = query.where(Task.title.like(f"%{search}%"))

    if done is not None:
        query = query.where(Task.done == done)

    query = query.order_by(Task.title)

    get_all_task = session.exec(query).all()
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


def get_stats(session: Session):
    total = session.exec(select(func.count(Task.id))).one()
    done = session.exec(select(func.count(Task.id)).where(Task.done == True)).one()
    return {"total": total, "done": done, "open": total - done}
