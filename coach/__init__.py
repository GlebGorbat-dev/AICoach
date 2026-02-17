import traceback
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI со всеми маршрутами и middleware."""
    app = FastAPI()

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Return error details in 500 response for debugging (check Network → Response)."""
        from fastapi import HTTPException as FastAPIHTTPException
        if isinstance(exc, FastAPIHTTPException):
            raise exc
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__,
                "traceback": traceback.format_exc(),
            },
        )

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