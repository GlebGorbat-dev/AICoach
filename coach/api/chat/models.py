
from datetime import datetime

from pydantic import Field

from coach.core.database import MongoBaseModel

class ChatModel(MongoBaseModel):
    title: str = 'New Chat'
    userId: str
    datetimeInserted: datetime = Field(default_factory=datetime.now)
    datetimeUpdated: datetime = Field(default_factory=datetime.now)