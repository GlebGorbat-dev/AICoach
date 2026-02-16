import asyncio

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mongodb import MongoDBChatMessageHistory

from coach.api.agent.db_requests import save_messages
from coach.api.agent.services.coach.tools import query_semantic_tool, search_tool, repl_tool
from coach.api.agent.services.prompts import coach_prompts
from coach.core.config import settings

class CoachAgent:
    def __init__(self, message_history: MongoDBChatMessageHistory, last_3_msg: list, prompt_template: str):
        """Инициализирует агента: подготавливает историю, инструменты и шаблон промпта."""
        if prompt_template is None:
            prompt_template = coach_prompts.agent_prompts.system_prompt
        self.message_history = message_history
        # Обработка случая, когда last_3_msg может быть None или пустым
        if last_3_msg is None:
            last_3_msg = []
        self.flat_msgs = [msg for m in last_3_msg for msg in (m if isinstance(m, list) else [m])]
        self.tools = [
            query_semantic_tool,
            search_tool,
            repl_tool,
        ]
        self.LLM = settings.LLM.bind_tools(tools=self.tools)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=prompt_template),
                *self.flat_msgs,
                ("human", "{content}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        agent = create_tool_calling_agent(
            llm=self.LLM,
            prompt=self.prompt,
            tools=self.tools
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
        )

    async def run(self, content: str) -> str:
        """Запускает обработку пользовательского запроса и возвращает текст ответа."""
        response = await self.agent_executor.ainvoke({"content": content})
        asyncio.create_task(save_messages(content, response, self.message_history))
        return response["output"][-1]["text"]