from pydantic_xml import BaseXmlModel, attr, element
from pydantic import ConfigDict
from datetime import datetime
from typing import List, Optional


class SummaryMarks(BaseXmlModel, tag="summary-marks", search_mode="unordered"):
    model_config = ConfigDict(extra="ignore")
    available: int = attr(name="available")
    obtained: int = attr(name="obtained")

# names are marked optional in case they don't get scanned properly by the marking machine
class MCQTestResult(BaseXmlModel, tag="mcq-test-result", search_mode="unordered"):
    model_config = ConfigDict(extra="ignore")
    scanned_on: datetime = attr(name="scanned-on")
    first_name: Optional[str] = element(tag="first-name")
    last_name: Optional[str] = element(tag="last-name")
    student_number: str = element(tag="student-number")
    test_id: int = element(tag="test-id")
    # answer: Optional[str] = element(tag="answer")
    summary_marks: Optional[SummaryMarks] = element(tag='summary-marks')




class ImportMarksRequest(BaseXmlModel, tag="mcq-test-results", search_mode="unordered"):
    model_config = ConfigDict(extra="ignore")
    mcq_test_results: List[MCQTestResult] = element(tag="mcq-test-result")
