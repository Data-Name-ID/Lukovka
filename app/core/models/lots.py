from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import BigInteger, Column, Enum, Field, Relationship

from core.db import BaseSQLModel
from core.models.depots import Depot, DepotPublic
from core.models.fuels import Fuel, FuelPublic

if TYPE_CHECKING:
    from app.core.models.orders import Order


class LotStatusEnum(StrEnum):
    CONFIRMED = "Подтверждён"
    SOLD_OUT = "Продан"


class LotBase(BaseSQLModel):
    deactivated_at: datetime
    current_volume: float
    price_per_ton: float


class Lot(LotBase, table=True):
    __tablename__ = "lots"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    initial_volume: float
    status: LotStatusEnum = Field(
        sa_column=Column(Enum(LotStatusEnum, name="lot_status")),
    )

    depot_id: int | None = Field(default=None, foreign_key="depots.id")
    depot: Depot | None = Relationship(back_populates="lots")

    fuel_id: int | None = Field(default=None, foreign_key="fuels.id")
    fuel: Fuel | None = Relationship(back_populates="lots")

    orders: list["Order"] = Relationship(back_populates="lot")


class LotPublic(LotBase):
    id: int

    depot: DepotPublic
    fuel: FuelPublic


class LotWithPages(BaseModel):
    page_count: int
    lots: list[LotPublic]
