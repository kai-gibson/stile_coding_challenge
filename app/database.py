from sqlmodel import create_engine, Session
import os

DB_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5432/markrdb"
)
engine = create_engine(DB_URL)


def get_session():
    with Session(engine) as session:
        yield session
