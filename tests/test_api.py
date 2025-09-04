# integration tests for /import
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool, select
from app.main import app
from app.models.results import Results
from app.database import get_session
from datetime import datetime


@pytest.fixture()
def session():
    # Test database, static pool so it persists
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=True,
        poolclass=StaticPool,
    )

    # Create tables
    Results.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override dependency of db session with test
    app.dependency_overrides[get_session] = get_test_session

    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    return TestClient(app)


def test_import_marks_success(client):
    post_body = """
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

    headers = {"Content-Type": "text/xml+markr"}
    response = client.post("/import", data=post_body, headers=headers)
    assert response.status_code == 200


def test_import_marks_failure_no_summary_marks(client):
    post_body = """
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
        </mcq-test-result>
    </mcq-test-results>
    """

    headers = {"Content-Type": "text/xml+markr"}
    response = client.post("/import", data=post_body, headers=headers)

    assert response.status_code == 400


def test_import_marks_success_update(client, session):
    post_body = """
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="16" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="10" />
        </mcq-test-result>
    </mcq-test-results>
    """

    headers = {"Content-Type": "text/xml+markr"}
    response = client.post("/import", data=post_body, headers=headers)

    stmt = select(Results).where(
        (Results.test_id == 1234) & (Results.student_number == 521585128)
    )
    result = session.exec(stmt).one_or_none()

    # Check that the first result was successfully overwritten by the second and not by the third
    assert result.obtained_marks == 16


def test_aggregate_results_one_result(client, session):
    # setup db with result in the example
    result = Results(
        student_number=1,
        test_id=1234,
        available_marks=20,
        obtained_marks=13,
        scanned_on=datetime.now(),
    )

    session.add(result)
    session.commit()

    aggregate_response = client.get("/results/1234/aggregate")

    assert (
        aggregate_response.text
        == '{"mean":65.0,"stddev":0.0,"min":65.0,"max":65.0,"p25":65.0,"p50":65.0,"p75":65.0,"count":1}'
    )


def test_aggregate_results_three_results(client, session):
    # setup db with result in the example
    results = [
        Results(
            student_number=1,
            test_id=1234,
            available_marks=20,
            obtained_marks=10,
            scanned_on=datetime.now(),
        ),
        Results(
            student_number=2,
            test_id=1234,
            available_marks=20,
            obtained_marks=15,
            scanned_on=datetime.now(),
        ),
        Results(
            student_number=3,
            test_id=1234,
            available_marks=20,
            obtained_marks=20,
            scanned_on=datetime.now(),
        ),
    ]

    session.add_all(results)
    session.commit()

    aggregate_response = client.get("/results/1234/aggregate")

    assert (
        aggregate_response.text
        == '{"mean":75.0,"stddev":20.41,"min":50.0,"max":100.0,"p25":62.5,"p50":75.0,"p75":87.5,"count":3}'
    )
