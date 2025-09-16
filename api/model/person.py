from pydantic import BaseModel

from uuid import UUID


class Person(BaseModel):
    """
    Person.
    :param id: person ID.
    :param name: person's full name.
    """
    id: UUID
    name: str
