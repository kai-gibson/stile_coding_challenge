# Markr - Stile Coding Challenge Submission
## Marking as a Service

This repo contains the code for a simple marking service built using Python and FastAPI. Python was selected due to its speed of prototyping and the stack of FastAPI, SQLAlchemy and pydantic were selected since they're reasonably quick (by python standards), are validation based, and industry standard ([See notes on performance](#notes-on-performance)).

The app uses a PostgreSQL database to store test results, since it's reasonably performant and supports concurrent writes.

## Usage
```
git clone https://github.com/kai-gibson/stile_coding_challenge.git
cd stile_coding_challenge
docker-compose up --build
```

Or to run manually:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4567
```

To run tests:
```
pytest
```

The service serves 2 endpoints:

## Endpoints
### Import
```
POST /import
```

Which accepts an XML payload with `Content-Type` `text/xml+markr` and returns a JSON
response on success or an error message on failure.

XML Payload:
```xml
    <mcq-test-results>
        <mcq-test-result scanned-on=datetime>
            <first-name>string</first-name>
            <last-name>string</last-name>
            <student-number>string</student-number>
            <test-id>int</test-id>
            <summary-marks available=int obtained=int />
        </mcq-test-result>
    </mcq-test-results>
```

If a record with the same `student-number` and `test-id` already exists, AND the
`available` or `obtained` marks are higher than the existing record, the record
will be updated.

If the `student-number`, `test-id`, or `summary-marks` fields are missing the
entire payload will be rejected with a 400 error.

### Aggregate
```
GET /results/{test-id}/aggregate
```
Which returns a JSON response with the aggregated test results for the given test id.

JSON Response:
```json
{
  "mean": float,
  "stddev": float,
  "min": float,
  "max": float,
  "p25": float,
  "p50": float,
  "p75": float,
  "count": int
}
```
If the `test-id` doesn't exist you will receive a 404 error


## Approach
This microservice has a single table:
```
class Results(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "student_number", "test_id", name="UNIQUE_CONSTRAINT_STUDENT_TEST_ID"
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    student_number: str
    test_id: int
    available_marks: int
    obtained_marks: int
    scanned_on: datetime
```
To note:
* Integer primary key for indexing
* Only identifier for a student is student ID stored in DB, no additional personal information
* Scanned on included in case we want to filter by date/time later
* marks stored as integers – delay floating point issues until data processing on `/results`
* Student ID is a string since the examples had leading some leading zeros, this may slow the query

`/import` essentially just validates the sent XML against the xml schema in `models/import_marks_request.py` and inserts each result into the database. Before inserting it checks if an existing result is in the DB and whether the `obtained` or `available` marks are lower and updating if so.

Then `/results` queries the DB for the available/obtained marks for the given test-id, transforms it into a list of scores out of 100.0, then uses numpy to create the statistics for the output JSON


## Assumptions
* The XML payload will contain the [fields noted under import](#import), and ignore any additional fields
* The /aggregate response should contain standard deviation, minimum, and maximum in addition to the mean, count, and percentiles – since the example response contained these
* `answer` field will be ignored for this prototype.
* `student-number`'s are unique per student, and should be treated as a string since they can have leading zeros.
* `test-id` is an integer and is unique per test.
* If an error occurs when updating/inserting the test-results on /import we should roll back all changes
* All float values in the /results endpoint are rounded to 2 decimal places. This is using python's default "bankers rounding" (.005 rounds down). If this is an issue for the visualisation team I can change it after the demo.

## Notes on Performance
Python is slow. Specifically loops and object creation are painfully slow, and due to the GIL threads (fastAPI will usually spin up a thread per request) aren't truly parallel which will likely pose issues at scale. The IO-bound performance issues could be mitigated by use of async, but the data processing will still be slow.

Given more time, and if real-time data visualisation was a hard requirement, I would likely have written this in a compiled language where you can better optimise heavy data processing (probably Go or Rust). 

Particular hot spots are likely:
* The `Results` table object creation, checking for existing rows and insertion/updating to the DB in a loop in the `/import` endpoint 
* The list comprehension to get % marks per student in `/results`. 

The numpy processing of these marks shouldn't be too bad but we'll need to profile to really see.