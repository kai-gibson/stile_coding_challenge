# Markr - Stile Coding Challenge Submission
## Marking as a Service

This repo contains the code for a simple marking service build using python and FastAPI. 
It uses a postgreSQL database to store test results, since it's reasonably performant and supports concurrent writes - useful since FastAPI will spin up a thread per request.


## Usage:
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

## Endpoints:
### Import
```
POST /import
```

Which accepts an XML payload of type `text/xml+markr` and returns a JSON
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
If the `test-id` doesn't exist you will recieve a 404 error

## Assumptions:
- The XML payload will at least contain `student-number`, `test-id`, and `summary-marks`
- The /aggregate response should contain standard deviation, minimum, and maximum in addition to the mean, count, and percentiles.
- `answer` field will be ignored for this prototype.
- `student-number`'s are unique per student, and should be treated as a string since they can have leading zeros.
- `test-id` is an integer and is unique per test.
- If an error occurs when updating/inserting the test-results on /import we should roll back all changes
