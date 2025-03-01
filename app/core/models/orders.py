from datetime import datetime
from enum import StrEnum

from sqlmodel import TIMESTAMP, BigInteger, Column, Enum, Field, Relationship, text

from core.db import BaseSQLModel
from core.models.lots import Lot, LotPublic
from core.models.user import User, UserPublic


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


class OrderFields(BaseSQLModel):
    status: OrderStatusEnum = Field(
        sa_column=Column(Enum(OrderStatusEnum, name="status")),
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

    lot: Lot | None = Relationship(back_populates="orders")

    user_id: int | None = Field(default=None, foreign_key="users.id")
    user: User | None = Relationship(back_populates="orders")


class OrderPublic(OrderBase, OrderFields):
    id: int

    lot: LotPublic
    user: UserPublic
