from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI со всеми маршрутами и middleware."""
    app = FastAPI()

    from coach.api.chat import chat_router
    app.include_router(chat_router, tags=["chat"])

    from coach.api.agent import agent_router
    app.include_router(agent_router, tags=["agent"])

    from coach.api.account import user_router
    app.include_router(user_router, tags=["user"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def read_root():
        """Возвращает базовый ответ сервиса для проверки доступности API."""
        return {"report": "Hello world!"}

    return app