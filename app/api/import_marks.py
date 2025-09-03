from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.results import Results
from app.models.import_marks_request import ImportMarksRequest

router = APIRouter()

@router.post("/import")
async def import_marks(request: Request, session: Session = Depends(get_session)):
    body_bytes = await request.body()
    content_type = request.headers.get("content-type", "")
    if "text/xml+markr" not in content_type:
        raise HTTPException(status_code=415, detail="Incorrect media type") 

    body = ImportMarksRequest.from_xml(body_bytes)
    print(body)
    return {"test":"message"}
