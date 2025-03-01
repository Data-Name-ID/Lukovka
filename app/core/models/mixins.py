from sqlmodel import BigInteger, Column, Field

from core.db import BaseSQLModel


class IDMixin(BaseSQLModel):
    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )
