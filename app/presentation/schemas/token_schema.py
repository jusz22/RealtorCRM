from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: datetime = None
