from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.results import Results
from app.models.aggregate_response import AggregateResponse

router = APIRouter()


@router.get("/results/{test_id}/aggregate")
def aggregate_marks(test_id: int, session: Session = Depends(get_session)):
    stmt = (
        select(Results)
        .where(Results.test_id == test_id)
    )

    results = session.exec(stmt).all()

    percent_marks = [
        (result.obtained_marks / result.available_marks) * 100 if result.available_marks else 0 
        for result in results
    ]

    print(percent_marks)

    response: AggregateResponse
    return {"test": "message"}
