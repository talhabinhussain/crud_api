from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv(override=True)


db_url = os.getenv("DATABASE_URL")


engine = create_engine(db_url)


def create_db_table():
    SQLModel.metadata.create_all(engine)


def get_sessin():
    with Session(engine) as session:
        yield session
