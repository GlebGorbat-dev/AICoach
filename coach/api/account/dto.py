from pydantic import BaseModel


class Account(BaseModel):
    email: str
    account_id: str