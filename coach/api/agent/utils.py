import json
from json import JSONDecodeError
from typing import List

from langchain_core.messages import AIMessage, HumanMessage

from coach.core.config import settings


async def get_amount_of_docs() -> int:
    """Возвращает количество документов, загруженных во векторное хранилище OpenAI."""
    if not settings.VS_ID or not settings.VS_ID.startswith('vs_'):
        raise ValueError(
            f"VS_ID должен быть валидным ID векторного хранилища OpenAI (начинается с 'vs_'). "
            f"Текущее значение: {settings.VS_ID}. "
            f"Создайте векторное хранилище в OpenAI и укажите его ID в переменной окружения VS_ID."
        )
    files = settings.OPENAI_CLIENT.vector_stores.files.list(
        vector_store_id=settings.VS_ID
    )
    return len([file async for file in files])

def get_last_3_messages(channelId: str) -> List:
    """Извлекает из MongoDB последние три сообщения пользователя и ассистента для чата."""
    collection = settings.MONGO_CLIENT["Coach_deploy"]["messages"]

    cursor = collection.find(
        {
            "sessionId": channelId
        }
    ).sort("_id", -1).limit(100)

    human_messages = []
    ai_messages = []

    for doc in cursor:
        raw = doc.get("History")
        if not raw:
            continue

        try:
            parsed = json.loads(raw)
            msg_type = parsed.get("type")
            content = parsed.get("data", {}).get("content", "")

            if msg_type == "human" and len(human_messages) < 3:
                human_messages.append(HumanMessage(content=content))

            elif msg_type == "ai" and len(ai_messages) < 3:
                ai_messages.append(AIMessage(content=content))

            if len(human_messages) == 3 and len(ai_messages) == 3:
                break

        except (json.JSONDecodeError, KeyError):
            continue

    # Формирование результата после цикла
    human_messages.reverse()
    ai_messages.reverse()

    mixed = []
    for i in range(max(len(human_messages), len(ai_messages))):
        if i < len(human_messages):
            mixed.append(human_messages[i])
        if i < len(ai_messages):
            mixed.append(ai_messages[i])

    return mixed