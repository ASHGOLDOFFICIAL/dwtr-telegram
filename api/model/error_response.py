import enum

from pydantic import BaseModel


class ErrorStatus(enum.IntEnum):
    """Error status."""
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    UNAUTHENTICATED = 16
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15


class ErrorInfo(BaseModel):
    """Error info."""
    reason: str
    domain: str


class ErrorDetails(BaseModel):
    """Error details."""
    info: ErrorInfo | None


class ErrorResponse(BaseModel):
    """
    Error response from API.
    :param status: error status.
    :param message: human-readable message.
    :param details: details for error.
    """
    status: ErrorStatus
    message: str
    details: ErrorDetails
