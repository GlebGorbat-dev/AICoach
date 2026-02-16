import asyncio

from fastapi import HTTPException

from coach.api.account.model import UserModel
from coach.core.config import settings
from coach.core.security import verify_password

async def post_user_obj(email, password) -> UserModel:
    """Создаёт нового пользователя в базе, проверяя, что e-mail ещё не зарегистрирован."""
    user = UserModel(email=email, password=password)
    check = await settings.DB_CLIENT.users.find_one({"email": email})
    if check:
        raise HTTPException(status_code=409, detail="Email already exists")
    await settings.DB_CLIENT.users.insert_one(user.to_mongo())
    return user

async def auth_user_obj(email, password) -> UserModel | None:
    """Проверяет существующего пользователя по e-mail и валидирует пароль."""
    user = await settings.DB_CLIENT.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if verify_password(password, user["password"]):
        return UserModel(**user)
    raise HTTPException(status_code=401, detail="Incorrect password")