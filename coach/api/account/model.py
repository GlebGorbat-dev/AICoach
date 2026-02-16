from passlib.context import CryptContext
from pydantic import Field, field_validator

from coach.core.database import MongoBaseModel


class UserModel(MongoBaseModel):
    password: str | None = Field(exclude=True, default=None)
    email: str

    @field_validator('password', mode='before', check_fields=False)
    @classmethod
    def set_password_hash(cls, v):
        """Хэширует пароль пользователя, если он ещё не записан в формате bcrypt."""
        if not v.startswith("2b$"):
            return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(v)
        return v