from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import col, exists, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models.orders import Order, OrderCreate, OrderPublic
from core.models.user import User, UserCreate
from core.store import Store


class OrderAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_orders(
        *,
        session: AsyncSession,
        offset: int = 0,
        page: int = 10,
        fuel_type: str | None = None,
        depot: str | None = None,
        region: str | None = None,
    ) -> bool | None:
        stmt = (
            select(OrderPublic)
            .where(
                (OrderPublic.fuel == fuel_type if fuel_type else True)
                & (OrderPublic.depot == depot if depot else True)
                & (OrderPublic.region == region if region else True),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )
        return await session.scalar(stmt)

    @staticmethod
    async def get_order_by_id(session: AsyncSession, order_id: int) -> bool | None:
        stmt = select(exists().where(col(User.id) == order_id))
        return await session.scalar(stmt)

    @staticmethod
    async def create_order(
        *,
        user_id: int,
        order_in: OrderCreate,
        session: AsyncSession,
    ) -> Order:
        stmt = (
            insert(Order)
            .values(
                **order_in.model_dump(),
                user_id=user_id,
            )
            .returning(Order)
        )
        return await session.scalar(stmt)
