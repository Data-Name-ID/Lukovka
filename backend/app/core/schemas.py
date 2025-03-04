from pydantic import BaseModel


class MessageScheme(BaseModel):
    message: str


class DetailScheme(BaseModel):
    detail: str
