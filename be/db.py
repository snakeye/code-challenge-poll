import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = os.getenv("DATABASE_URL", f"sqlite:///{sqlite_file_name}")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

__all__ = [
    "engine",
    "create_db_and_tables",
    "get_session",
    "SessionDep",
]
