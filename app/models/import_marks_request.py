from pydantic_xml import BaseXmlModel, attr, element
from pydantic import Field
from datetime import datetime
from typing import List, Optional


class SummaryMarks(BaseXmlModel, tag="summary-marks"):
    available: int = attr(name="available")
    obtained: int = attr(name="obtained")


# names are marked optional in case they don't get scanned properly by the marking machine
class MCQTestResult(BaseXmlModel, tag="mcq-test-result"):
    scanned_on: datetime = attr(name="scanned-on")
    first_name: Optional[str] = element(tag="first-name")
    last_name: Optional[str] = element(tag="last-name")
    student_number: str = element(tag="student-number")
    test_id: int = element(tag="test-id")
    summary_marks: SummaryMarks = element()


class ImportMarksRequest(BaseXmlModel, tag="mcq-test-results"):
    mcq_test_results: List[MCQTestResult] = element(tag="mcq-test-result")
