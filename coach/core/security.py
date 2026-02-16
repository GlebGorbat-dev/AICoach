
from datetime import timedelta, datetime
from typing import Optional, Callable

from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from coach.core.config import settings
from coach.api.account.dto import Account

def verify_password(plain_password, hashed_password) -> bool:
    result = CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)
    return result

def create_access_token(email: str, account_id: str):
    payload = {
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name": email,
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": account_id,
        "accountId": account_id,
        "exp": datetime.utcnow() + timedelta(days=30)
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_verify_token(auto_error: bool = True) -> Callable:
    """Возвращает зависимость FastAPI для проверки JWT-токена в запросах."""
    security = HTTPBearer(auto_error=auto_error)

    async def verify_token(
            credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    ) -> Optional[Account]:
        """Валидирует JWT из заголовка и возвращает данные аккаунта."""
        if not credentials:
            return None

        token = credentials.credentials
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"],)

            email = payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name")
            account_id = payload.get("accountId")
        except Exception:
            raise HTTPException(status_code=403, detail=f"Invalid credentials.")

        if email is None or account_id is None:
            raise HTTPException(status_code=403, detail="Permission denied")

        return Account(account_id=account_id, email=email)

    return verify_token