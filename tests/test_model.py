import pytest
from app.models.import_marks_request import ImportMarksRequest


# from example
xml_data = """
<mcq-test-results>
    <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
        <first-name>Jane</first-name>
        <last-name>Austen</last-name>
        <student-number>521585128</student-number>
        <test-id>1234</test-id>
        <summary-marks available="20" obtained="13" />
    </mcq-test-result>
</mcq-test-results>
"""

def test_import_marks_request():
    request = ImportMarksRequest.from_xml(xml_data)

    assert len(request.mcq_test_results) == 1

    result = request.mcq_test_results[0]
    assert result.first_name == "Jane"
    assert result.last_name == "Austen"
    assert result.test_id == 1234
    assert result.summary_marks.available == 20
    assert result.summary_marks.obtained == 13
