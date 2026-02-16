
from coach.api.account import user_router
from coach.api.account.db_requests import post_user_obj, auth_user_obj
from coach.api.account.schemas import RegisterRequest, TokenResponse
from coach.core.security import create_access_token
from coach.core.wrappers import CoachResponseWrapper

@user_router.post("/register")
async def register_user(
        request: RegisterRequest
) -> CoachResponseWrapper[TokenResponse]:
    """Регистрирует нового пользователя и возвращает токен доступа."""
    user = await post_user_obj(request.email, request.password)
    token = create_access_token(user.email, user.id)
    return CoachResponseWrapper(data=TokenResponse(token=token))

@user_router.post("/login")
async def login_user(
        request: RegisterRequest
) -> CoachResponseWrapper[TokenResponse]:
    """Авторизует пользователя по e-mail и паролю и формирует токен."""
    user = await auth_user_obj(request.email, request.password)
    token = create_access_token(user.email, user.id)
    return CoachResponseWrapper(data=TokenResponse(token=token))
