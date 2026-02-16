
from langchain_community.tools import tool, Tool
from langchain_experimental.utilities import PythonREPL

from coach.api.agent.services.prompts import coach_prompts
from coach.core.config import settings

@tool
async def query_semantic_tool(query: str) -> str:
    """Опциональный инструмент: ищет релевантные текстовые фрагменты в векторном хранилище для специализированных вопросов о движении, упражнениях и восстановлении. Используй этот инструмент ТОЛЬКО если вопрос связан с этими темами. Для всех остальных вопросов отвечай напрямую, не используя этот инструмент."""
    try:
        prompt = coach_prompts.vector_search.prompt.format(input_query=query)
        response = await settings.OPENAI_CLIENT.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            max_tool_calls=1,
            temperature=0.0,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [settings.VS_ID],
                "max_num_results": 2
            }]
        )

        return response.output_text
    except Exception as e:
        print(f"[query_semantic_tool] Error: {e}")
        return "Nothing found."

search_tool = settings.TAVILY_TOOL

python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)