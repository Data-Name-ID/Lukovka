from sqlmodel import BigInteger, Column, Field

from core.db import BaseSQLModel


class DepotBase(BaseSQLModel):
    name: str


class Depot(DepotBase, table=True):
    __tablename__ = "depots"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )


class DepotPublic(DepotBase):
    id: int
