from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel
from sqlmodel import BigInteger, Column, Enum, Field, Relationship

from core.db import BaseSQLModel
from core.models.depots import DepotPublic
from core.models.fuels import FuelPublic


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
    fuel_id: int | None = Field(default=None, foreign_key="fuels.id")


class LotPublic(LotBase):
    id: int

    depot: DepotPublic
    fuel: FuelPublic


class LotWithPages(BaseModel):
    page_count: int
    lots: list[LotPublic]
