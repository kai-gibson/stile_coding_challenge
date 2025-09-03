from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models.results import Results

router = APIRouter()

@router.post("/import")
def import_marks(session: Session = Depends(get_session)):
    return {"test":"message"}
