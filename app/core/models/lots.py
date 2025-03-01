from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel
from sqlmodel import BigInteger, Column, Enum, Field, Relationship

from core.db import BaseSQLModel
from core.models.depots import Depot, DepotPublic
from core.models.fuels import Fuel, FuelPublic


class LotStatusEnum(StrEnum):
    CONFIRMED = "Подтверждён"
    SOLD_OUT = "Продан"


class LotBase(BaseSQLModel):
    price: float
    current_volume: float

    status: LotStatusEnum = Field(
        sa_column=Column(Enum(LotStatusEnum, name="lot_status")),
    )


class LotCreate(LotBase):
    initial_volume: float
    date: datetime

    depot_id: int = Field(foreign_key="depots.id")
    fuel_id: int = Field(foreign_key="fuels.id")


class Lot(LotCreate, table=True):
    __tablename__ = "lots"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    depot: Depot | None = Relationship(back_populates="lots")
    fuel: Fuel | None = Relationship(back_populates="lots")


class LotPublic(LotBase):
    id: int

    depot: str
    fuel: str
    region: str


class LotWithPages(BaseModel):
    page_count: int
    lots: list[LotPublic]
