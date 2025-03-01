from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel
from sqlmodel import BigInteger, Column, Enum, Field

from core.db import BaseSQLModel
from core.models.depots import DepotPublic
from core.models.fuels import FuelPublic


class LotStatusEnum(StrEnum):
    CONFIRMED = "Подтверждён"
    SOLD_OUT = "Продан"


class LotBase(BaseSQLModel):
    date: datetime
    price: float


class LotCreate(LotBase):
    initial_volume: float
    current_volume: float

    status: LotStatusEnum = Field(
        sa_column=Column(Enum(LotStatusEnum, name="lot_status")),
    )

    depot_id: int = Field(foreign_key="depots.id")
    fuel_id: int = Field(foreign_key="fuels.id")


class Lot(LotCreate, table=True):
    __tablename__ = "lots"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )


class LotPublic(LotBase):
    id: int

    depot: DepotPublic
    fuel: FuelPublic


class LotWithPages(BaseModel):
    page_count: int
    lots: list[LotPublic]
