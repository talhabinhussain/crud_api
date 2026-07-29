from sqlmodel import Session, func, select

from app.models.task_model import Task


def all_task(session: Session):
    return session.exec(select(Task)).all()


def get_id(id: int, session: Session):
    return session.get(Task, id)


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
