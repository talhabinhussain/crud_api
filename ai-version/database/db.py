from sqlmodel import SQLModel, Session, create_engine


db_url = "sqlite:///task.db"

engine = create_engine(db_url)


def create_db_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
