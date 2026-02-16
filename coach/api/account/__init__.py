from fastapi.routing import APIRouter

user_router = APIRouter(
    prefix="/api/user", tags=["user"]
)

from . import views