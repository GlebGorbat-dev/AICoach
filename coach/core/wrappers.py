from functools import wraps
from typing import Generic, Optional, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

T = TypeVar('T')

class ErrorCoachResponse(BaseModel):
    message: str

class CoachResponseWrapper(BaseModel, Generic[T]):
    data: Optional[T] = None
    successful: bool = True
    error: Optional[ErrorCoachResponse] = None

    def response(self, status_code: int):
        """Формирует стандартизированный JSON-ответ с заданным статусом."""
        return JSONResponse(
            status_code=status_code,
            content={
                "data": self.data,
                "successful": self.successful,
                "error": self.error.dict() if self.error else None
            }
        )

def exception_wrapper(http_error: int, error_message: int):
    """Оборачивает корутину, чтобы превращать исключения в HTTP ошибки."""
    def decorator(func):
        """Создаёт декоратор для обработки ошибок вызываемой функции."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """Вызывает целевую функцию и перехватывает исключения, заменяя их HTTPError."""
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=http_error, detail=error_message) from e

        return wrapper

    return decorator

def background_task():
    """Создаёт декоратор для безопасного запуска фоновой асинхронной задачи."""
    def decorator(func):
        """Возвращает обёртку, которая подавляет ошибки фоновой функции."""
        @wraps(func)
        async def wrapper(*args, **kwargs) -> str:
            """Запускает функцию и игнорирует исключения, чтобы не прерывать фоновые задачи."""
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                pass

        return wrapper

    return decorator
