from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel
from sqlmodel import TIMESTAMP, BigInteger, Column, Enum, Field, Relationship, text

from core.db import BaseSQLModel
from core.models.lots import Lot
from core.models.user import User


class DeliveryTypeEnum(StrEnum):
    DELIVERY = "Доставка"
    SELF_PICKUP = "Самовывоз"


class OrderStatusEnum(StrEnum):
    CONFIRMED = "Подтверждён"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Выполнен"
    CANCELED = "Отменён"


class OrderBase(BaseSQLModel):
    volume: float

    delivery_type: DeliveryTypeEnum = Field(
        sa_column=Column(Enum(DeliveryTypeEnum, name="delivery_type")),
    )


class OrderCreate(OrderBase):
    lot_id: int | None = Field(default=None, foreign_key="lots.id")


class OrderUpdate(BaseModel):
    status: OrderStatusEnum


class OrderFields(BaseSQLModel):
    status: OrderStatusEnum = Field(
        default=OrderStatusEnum.IN_PROGRESS,
        sa_column=Column(
            Enum(OrderStatusEnum, name="status"),
            default=OrderStatusEnum.IN_PROGRESS,
        ),
    )

    created_datetime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_datetime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )


class Order(OrderCreate, OrderFields, table=True):
    __tablename__ = "orders"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    user_id: int | None = Field(default=None, foreign_key="users.id")

    lot: Lot = Relationship(back_populates="orders")
    user: User = Relationship(back_populates="orders")


class OrderPublic(OrderBase, OrderFields):
    id: int

    depot: str
    fuel: str
    region: str
    user_id: int


class OrderWithPages(BaseModel):
    page_count: int
    orders: list[OrderPublic]
