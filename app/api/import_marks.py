from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app.database import get_session
from app.models.results import Results
from app.models.import_marks_request import ImportMarksRequest

router = APIRouter()


@router.post("/import")
async def import_marks(request: Request, session: Session = Depends(get_session)):
    body_bytes = await request.body()
    content_type = request.headers.get("content-type", "")

    # return error on any other content type
    if "text/xml+markr" not in content_type:
        raise HTTPException(status_code=415, detail="Incorrect media type")

    # validate xml against pydantic schema
    try:
        body = ImportMarksRequest.from_xml(body_bytes)
    except ValidationError:
        raise HTTPException(400, detail="Invalid XML body")

    for test_result in body.mcq_test_results:
        stmt = (
            select(Results)
            .where(Results.test_id == test_result.test_id)
            .where(Results.student_number == test_result.student_number)
        )

        existing_result = session.exec(stmt).one_or_none()

        # if there's existing test results for this student and test_id, check if
        # the new obtained or available marks are higher than the last and update them in the db
        if existing_result is not None:
            if (
                existing_result.available_marks < test_result.summary_marks.available
                or existing_result.obtained_marks < test_result.summary_marks.obtained
            ):
                existing_result.available_marks = test_result.summary_marks.available
                existing_result.obtained_marks = test_result.summary_marks.obtained

                session.add(existing_result)

            else:
                continue  # if newly scanned marks are lower than the previous, skip
        else:
            new_result = Results(
                student_number=test_result.student_number,
                test_id=test_result.test_id,
                available_marks=test_result.summary_marks.available,
                obtained_marks=test_result.summary_marks.obtained,
                scanned_on=test_result.scanned_on,
            )

            session.add(new_result)

    # commit all the updates/inserts together and roll back on failure - to avoid partial updates
    try:
        session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(500, detail=f"Error updating database: {str(e)}")

    return {"detail": "Update successful"}
