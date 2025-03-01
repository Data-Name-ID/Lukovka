from pydantic import BaseModel


class OrderFilterParams(BaseModel):
    page: int = 10
    offset: int = 1
    fuel: str | None = None
    depot: str | None = None
    region: str | None = None
    status: str | None = None
    user_id: int | None = None
