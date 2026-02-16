
from enum import Enum

from pydantic import BaseModel


class Paging(BaseModel):
    pageSize: int
    pageIndex: int
    totalCount: int


class Author(Enum):
    User = "human"
    Assistant = "ai"


class Message(BaseModel):
    role: Author
    content: str
