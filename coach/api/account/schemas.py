from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    token: str