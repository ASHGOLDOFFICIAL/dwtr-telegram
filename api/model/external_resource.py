
import enum
from pydantic import BaseModel


class ExternalResourceType(enum.StrEnum):
    """Type of links to external resource."""
    PURCHASE = "purchase"
    STREAMING = "streaming"
    DOWNLOAD = "download"
    OTHER = "other"
    PRIVATE = "private"


class ExternalResource(BaseModel):
    """Link to an external resource."""
    resource_type: ExternalResourceType
    link: str
