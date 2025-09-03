from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(
    "postgresql://postgres:password@localhost:5432/markrdb", echo=True
)

def get_session():
    with Session(engine) as session:
        yield session
