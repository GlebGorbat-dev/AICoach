
from fastapi.routing import APIRouter

chat_router = APIRouter(
    prefix="/api/chat", tags=["chat"]
)

from . import views
