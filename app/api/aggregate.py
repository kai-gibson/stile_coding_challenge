from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.results import Results
from app.models.aggregate_response import AggregateResponse
import numpy as np
import math

router = APIRouter()

@router.get("/results/{test_id}/aggregate")
def aggregate_marks(test_id: int, session: Session = Depends(get_session)):
    stmt = select(Results).where(Results.test_id == test_id)

    results = session.exec(stmt).all()
    if len(results) == 0:
        raise HTTPException(404, detail=f"No results found for test-id {test_id}")

    # Get list of percentage marks i.e. 90.0 == 90%
    percent_marks = [
        (result.obtained_marks / result.available_marks) * 100
        if result.available_marks
        else 0
        for result in results
    ]

    print(percent_marks)

    percentiles = np.percentile(percent_marks, [25, 50, 75])
    response = AggregateResponse(
        mean=round(float(np.mean(percent_marks)), 2),
        stddev=round(float(np.std(percent_marks, ddof=0)), 2),
        min=round(float(np.min(percent_marks)), 2),
        max=round(float(np.max(percent_marks)), 2),
        p25=round(float(percentiles[0]), 2),
        p50=round(float(percentiles[1]), 2),
        p75=round(float(percentiles[2]), 2),
        count=len(percent_marks),
    )

    print(response)

    return response
