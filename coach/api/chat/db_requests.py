
import asyncio

from fastapi import HTTPException

from coach.api.chat.models import ChatModel
from coach.api.chat.schemas import ChatTitleRequest

from coach.core.config import settings


async def get_chat_obj(chat_id: str, user_id: str) -> ChatModel:
    """Находит чат пользователя по идентификаторам и выбрасывает ошибку, если он не найден."""
    find_query = {"id": chat_id, "userId": user_id} if user_id != settings.ADMIN_ID else {"id": chat_id}
    chat = await settings.DB_CLIENT.chats.find_one(find_query)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatModel.from_mongo(chat)


async def create_chat_obj(user_id: str) -> ChatModel:
    """Создаёт новый чат для указанного пользователя и сохраняет его в базе."""
    chat = ChatModel(userId=user_id)
    await settings.DB_CLIENT.chats.insert_one(chat.to_mongo())
    return chat


async def delete_chat_obj(chat_id: str, user_id: str) -> None:
    """Удаляет чат пользователя после проверки права доступа."""
    find_query = {"id": chat_id, "userId": user_id} if user_id != settings.ADMIN_ID else {"id": chat_id}
    chat = await settings.DB_CLIENT.chats.find_one(find_query)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    await settings.DB_CLIENT.chats.delete_one({"id": chat_id})


async def update_chat_obj_title(chat_id: str, chat_request: ChatTitleRequest, user_id: str) -> ChatModel:
    """Обновляет заголовок чата и возвращает обновлённую модель."""
    find_query = {"id": chat_id, "userId": user_id} if user_id != settings.ADMIN_ID else {"id": chat_id}
    chat = await settings.DB_CLIENT.chats.find_one(find_query)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat = ChatModel.from_mongo(chat)
    chat.title = chat_request.title
    await settings.DB_CLIENT.chats.update_one({"id": chat_id}, {"$set": chat.to_mongo()})
    return chat


async def get_all_chats_obj(page_size: int, page_index: int, user_id: str) -> tuple[list[ChatModel], int]:
    """Возвращает список чатов постранично и общее количество записей."""
    skip = page_size * page_index
    filter_query = {} if user_id == settings.ADMIN_ID else {"userId": user_id}
    objects, total_count = await asyncio.gather(
        settings.DB_CLIENT.chats
        .find(filter_query)
        .sort("_id", -1)
        .skip(skip)
        .limit(page_size)
        .to_list(length=page_size),
        settings.DB_CLIENT.chats.count_documents({}),
    )
    return objects, total_count
