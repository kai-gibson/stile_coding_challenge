from fastapi import FastAPI
from sqlmodel import SQLModel
from app.models.results import Results
from app.api import aggregate, import_marks
from app.database import engine

app = FastAPI()


# In future I'd make this app use fastAPI lifespan for startup, for this prototype this is fine
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)


app.include_router(import_marks.router)
app.include_router(aggregate.router)
