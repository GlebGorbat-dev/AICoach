
from typing import Optional

from pydantic import BaseModel

from coach.api.chat.dto import Paging, Message
from coach.api.chat.models import ChatModel
from coach.core.wrappers import CoachResponseWrapper

class PromptTextRequest(BaseModel):
    text: str
    promptTemplate: Optional[str] = None

class AgentResponse(BaseModel):
    text: str | None = None


class AmountOfDocumentsResponse(BaseModel):
    amountOfDocuments: int

class AllMessagesResponse(BaseModel):
    paging: Paging
    data: list[Message]


class AllChatResponse(BaseModel):
    paging: Paging
    data: list[ChatModel]


class AllChatWrapper(CoachResponseWrapper[AllChatResponse]):
    pass


class ChatTitleRequest(BaseModel):
    title: str

