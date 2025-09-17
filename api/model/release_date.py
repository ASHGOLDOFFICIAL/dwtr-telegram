from datetime import date

import enum
from pydantic import BaseModel


class DateAccuracy(enum.StrEnum):
    """Degree of release date accuracy."""
    FULL = "full"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class ReleaseDate(BaseModel):
    """Release date of something."""
    date: date
    accuracy: DateAccuracy
