
from typing import Optional

from fastapi import Query, Depends

from coach.api.account.dto import Account
from coach.api.chat import chat_router
from coach.api.chat.db_requests import (get_chat_obj,
                                           delete_chat_obj,
                                           update_chat_obj_title,
                                           create_chat_obj,
                                           get_all_chats_obj)
from coach.api.chat.dto import Paging
from coach.api.chat.models import ChatModel
from coach.api.chat.schemas import ChatTitleRequest, AllChatWrapper, AllChatResponse
from coach.core.security import get_verify_token
from coach.core.wrappers import CoachResponseWrapper

@chat_router.get("/all")
async def get_all_chats(
        pageSize: Optional[int] = Query(10, description="Number of objects to return per page"),
        pageIndex: Optional[int] = Query(0, description="Page index to retrieve"),
        account: Account = Depends(get_verify_token()),
) -> AllChatWrapper:
    """Возвращает список чатов пользователя с пагинацией."""
    chats, total_count = await get_all_chats_obj(pageSize, pageIndex, account.account_id)
    response = AllChatResponse(
        paging=Paging(pageSize=pageSize, pageIndex=pageIndex, totalCount=total_count),
        data=chats
    )
    return AllChatWrapper(data=response)

@chat_router.get("/{chatId}")
async def get_chat(
        chatId: str,
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper[ChatModel]:
    """Получает данные конкретного чата по идентификатору."""
    chat = await get_chat_obj(chatId, account.account_id)
    return CoachResponseWrapper(data=chat)

@chat_router.delete("/{chatId}")
async def delete_chat(
        chatId: str,
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper:
    """Удаляет указанный чат пользователя."""
    await delete_chat_obj(chatId, account.account_id)
    return CoachResponseWrapper()

@chat_router.patch("/{chatId}/title")
async def update_chat_title(
        chatId: str,
        chat: ChatTitleRequest,
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper[ChatModel]:
    """Обновляет заголовок существующего чата."""
    chat = await update_chat_obj_title(chatId, chat, account.account_id)
    return CoachResponseWrapper(data=chat)

@chat_router.post("")
async def create_chat(
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper[ChatModel]:
    """Создаёт новый чат для авторизованного пользователя."""
    chat = await create_chat_obj(account.account_id)
    return CoachResponseWrapper(data=chat)
