from sqlmodel import BigInteger, Column, Field

from core.db import BaseSQLModel


class FuelBase(BaseSQLModel):
    name: str


class Fuel(FuelBase, table=True):
    __tablename__ = "fuels"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )


class FuelPublic(FuelBase):
    id: int
