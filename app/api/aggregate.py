from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session

router = APIRouter()


@router.get("/results/{test_id}/aggregate")
def aggregate_marks(test_id: int, session: Session = Depends(get_session)):
    return {"test": "message"}
