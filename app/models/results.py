from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
from datetime import datetime


class Results(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "student_number", "test_id", name="UNIQUE_CONSTRAINT_STUDENT_TEST_ID"
        ),
    )
    id: int = Field(primary_key=True)
    student_number: str
    test_id: int
    available_marks: int
    obtained_marks: int
    scanned_on: datetime
