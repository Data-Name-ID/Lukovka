from pydantic import BaseModel


class LotFilterParams(BaseModel):
    page: int = 1
    offset: int = 10
    fuel: str | None = None
    depot: str | None = None
    region: str | None = None
