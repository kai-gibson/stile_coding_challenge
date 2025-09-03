from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.results import Results
from app.models.aggregate_response import AggregateResponse
import numpy as np

router = APIRouter()

@router.get("/results/{test_id}/aggregate")
def aggregate_marks(test_id: int, session: Session = Depends(get_session)):
    stmt = select(Results).where(Results.test_id == test_id)

    results = session.exec(stmt).all()

    percent_marks = [
        (result.obtained_marks / result.available_marks) * 100
        if result.available_marks
        else 0
        for result in results
    ]

    print(percent_marks)

    percentiles = np.percentile(percent_marks, [25, 50, 75])
    response = AggregateResponse(
        mean=float(np.mean(percent_marks)),
        stddev=float(np.std(percent_marks, ddof=1)),
        min=np.min(percent_marks),
        max=np.max(percent_marks),
        p25=percentiles[0],
        p50=percentiles[1],
        p75=percentiles[2],
        count=len(percent_marks),
    )

    print(response)

    return response
