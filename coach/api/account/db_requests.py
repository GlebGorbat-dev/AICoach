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
    user_doc = await settings.DB_CLIENT.users.find_one({"email": email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found.")

    if not verify_password(password, user_doc["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # MongoDB returns _id, UserModel expects id (str)
    return UserModel(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        password=user_doc["password"],
    )