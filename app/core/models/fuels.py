from typing import TYPE_CHECKING

from sqlmodel import BigInteger, Column, Field, Relationship

from core.db import BaseSQLModel

if TYPE_CHECKING:
    from core.models.lots import Lot


class FuelBase(BaseSQLModel):
    name: str


class Fuel(FuelBase, table=True):
    __tablename__ = "fuels"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    lots: list["Lot"] = Relationship(back_populates="fuel")


class FuelPublic(FuelBase):
    id: int
