from enum import StrEnum, auto

from pydantic import BaseModel


class TokenType(StrEnum):
    ACCESS = auto()
    REFRESH = auto()
    EMAIL_CONFIRM = auto()
    RESET_PASSWORD = auto()


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Token(BaseModel):
    token: str
    jti: str


class TokenCollection(BaseModel):
    type: str = "Bearer"

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    typ: TokenType
    jti: str
    iat: float
    exp: float
    sub: str
    rjti: str | None = None
