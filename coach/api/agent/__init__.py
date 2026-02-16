from fastapi.routing import APIRouter

agent_router = APIRouter(
    prefix="/api/agent", tags=["agent"]
)

from . import views