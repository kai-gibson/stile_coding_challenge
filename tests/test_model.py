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
    assert result.student_number == "521585128"
    assert result.test_id == 1234
    assert result.summary_marks.available == 20
    assert result.summary_marks.obtained == 13

xml_data_from_sample = """
<mcq-test-results>
	<mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
		<first-name>KJ</first-name>
		<last-name>Alysander</last-name>
		<student-number>002299</student-number>
		<test-id>9863</test-id>
		<answer question="0" marks-available="1" marks-awarded="1">D</answer>
		<answer question="1" marks-available="1" marks-awarded="1">D</answer>
		<answer question="2" marks-available="1" marks-awarded="1">D</answer>
		<answer question="3" marks-available="1" marks-awarded="0">C</answer>
		<answer question="4" marks-available="1" marks-awarded="1">B</answer>
		<answer question="5" marks-available="1" marks-awarded="0">D</answer>
		<answer question="6" marks-available="1" marks-awarded="0">A</answer>
		<answer question="7" marks-available="1" marks-awarded="1">A</answer>
		<answer question="8" marks-available="1" marks-awarded="1">B</answer>
		<answer question="9" marks-available="1" marks-awarded="1">D</answer>
		<answer question="10" marks-available="1" marks-awarded="1">A</answer>
		<answer question="11" marks-available="1" marks-awarded="1">B</answer>
		<answer question="12" marks-available="1" marks-awarded="0">A</answer>
		<answer question="13" marks-available="1" marks-awarded="0">B</answer>
		<answer question="14" marks-available="1" marks-awarded="1">B</answer>
		<answer question="15" marks-available="1" marks-awarded="1">A</answer>
		<answer question="16" marks-available="1" marks-awarded="1">C</answer>
		<answer question="17" marks-available="1" marks-awarded="0">B</answer>
		<answer question="18" marks-available="1" marks-awarded="1">A</answer>
		<answer question="19" marks-available="1" marks-awarded="0">B</answer>
		<summary-marks available="20" obtained="13" />
	</mcq-test-result>
</mcq-test-results>
"""

def test_import_marks_single_from_sample():
    request = ImportMarksRequest.from_xml(xml_data_from_sample)

    assert len(request.mcq_test_results) == 1

    result = request.mcq_test_results[0]
    assert result.first_name == "KJ"
    assert result.last_name == "Alysander"
    assert result.student_number == "002299"
    assert result.test_id == 9863
    assert result.summary_marks.available == 20
    assert result.summary_marks.obtained == 13
    
def test_import_marks_sample_results():
    sample_data: str
    with open('sample_data/sample_results.xml', 'r') as sample_results:
        sample_data = sample_results.read()
    
    request = ImportMarksRequest.from_xml(sample_data)
    assert len(request.mcq_test_results) == 100