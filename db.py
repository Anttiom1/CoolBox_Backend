import contextlib
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("mysql+mysqlconnector://root:@localhost/coolbox")
db_session = sessionmaker(bind=engine)

def get_connection():
    conn = db_session()
    return conn

#Fastapi endpoint requires dependencies to be generators not context managers
def get_db():
    conn = None
    try:
        conn = db_session()
        yield conn
    finally:
        if conn is not None:
            conn.close()

#Use this context manager in inserting sensor data
db_context = contextlib.contextmanager(get_db)

DB = Annotated[Session, Depends(get_db)]