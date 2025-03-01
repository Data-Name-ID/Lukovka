from typing import TYPE_CHECKING

from sqlmodel import BigInteger, Column, Field, Relationship

from core.db import BaseSQLModel

if TYPE_CHECKING:
    from core.models.lots import Lot


class DepotBase(BaseSQLModel):
    name: str


class Depot(DepotBase, table=True):
    __tablename__ = "depots"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    lots: list["Lot"] = Relationship(back_populates="depot")


class DepotPublic(DepotBase):
    id: int
