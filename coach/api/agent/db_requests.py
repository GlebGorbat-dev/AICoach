import pydash

from langchain_core.messages import HumanMessage, AIMessage
from langchain_mongodb import MongoDBChatMessageHistory

from coach.core.config import settings

async def get_message_history(
        chatId: str
) -> MongoDBChatMessageHistory:
    """Возвращает историю сообщений для указанного чата из MongoDB."""
    message_history = MongoDBChatMessageHistory(
        session_id=f"{chatId}",
        client=settings.MONGO_CLIENT,
        connection_string=None,
        session_id_key="sessionId",
        database_name="Coach_deploy",
        collection_name="messages",
    )
    return message_history

async def save_messages(
        query: str, response: dict, message_history: MongoDBChatMessageHistory
) -> None:
    """Сохраняет запрос пользователя и ответ агента в историю сообщений."""
    # add_messages - синхронный метод, не требует await
    message_history.add_messages([
        HumanMessage(content=query),
        AIMessage(
            content=response["output"],
            additional_kwargs={"moduleResponse": pydash.get(response, "intermediate_steps[-1][-1]", None)}
        )
    ])