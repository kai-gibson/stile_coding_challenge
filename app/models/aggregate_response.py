from pydantic import BaseModel


"""
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
"""


class AggregateResponse(BaseModel):
    mean: float
    stddev: float
    min: float
    max: float
    p25: float
    p50: float
    p75: float
    count: int
