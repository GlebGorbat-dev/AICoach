
from langchain_core.messages import BaseMessage

from coach.api.chat.dto import Author, Message

def prepare_api_messages(messages: list[BaseMessage]) -> list[Message]:
    """Преобразует сообщения LangChain в формат API с ролями и текстом."""
    result = []
    for message in messages:
        if message.type == "human":
            content = message.content
        else:
            content = message.content[0]["text"]

        result.append(Message(content=content, role=Author(message.type)))

    return result