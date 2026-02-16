
import asyncio

from fastapi import Depends

from coach.api.account.dto import Account
from coach.api.agent import agent_router
from coach.api.agent.services import CoachAgent
from coach.api.agent.db_requests import get_message_history
from coach.api.agent.utils import get_amount_of_docs, get_last_3_messages
from coach.api.chat.db_requests import get_chat_obj
from coach.api.chat.dto import Paging
from coach.api.chat.schemas import AgentResponse, PromptTextRequest, AllMessagesResponse, AmountOfDocumentsResponse
from coach.api.chat.utils import prepare_api_messages
from coach.core.security import get_verify_token
from coach.core.wrappers import CoachResponseWrapper

@agent_router.get("/{chatId}/all")
async def get_all_chat_messages(
        chatId: str,
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper[AllMessagesResponse]:
    """Возвращает подготовленный список всех сообщений выбранного чата."""
    messages, check = await asyncio.gather(
        get_message_history(chatId),
        get_chat_obj(chatId, account.account_id)
    )
    messages = prepare_api_messages(messages.messages)
    response = AllMessagesResponse(
        paging=Paging(pageSize=len(messages), pageIndex=0, totalCount=len(messages)),
        data=messages
    )
    return CoachResponseWrapper(data=response)

@agent_router.post("/{chatId}")
async def create_message(
        chatId: str,
        prompt_request: PromptTextRequest,
        account: Account = Depends(get_verify_token())
) -> CoachResponseWrapper[AgentResponse]:
    """Запускает агента для генерации ответа на запрос пользователя и возвращает текст."""
    last_3_msg = get_last_3_messages(chatId)
    message_history, check = await asyncio.gather(
        get_message_history(chatId),
        get_chat_obj(chatId, account.account_id),
    )
    agent = CoachAgent(message_history, last_3_msg, prompt_request.promptTemplate)
    response = await agent.run(prompt_request.text)
    return CoachResponseWrapper(data=AgentResponse(text=response))

@agent_router.get("/documents")
async def get_amount_of_documents() -> CoachResponseWrapper[AmountOfDocumentsResponse]:
    """Сообщает количество документов, доступных агенту для поиска."""
    amount_of_documents = await get_amount_of_docs()
    return CoachResponseWrapper(data=AmountOfDocumentsResponse(amountOfDocuments=amount_of_documents))