from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import col, exists, select, update, true
from sqlmodel.ext.asyncio.session import AsyncSession

from api.auth.depends import UserDep
from core.models.orders import Order, OrderCreate, OrderPublic
from core.models.user import User, UserCreate
from core.store import Store


class OrderAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_orders(
        *,
        user: UserDep,
        session: AsyncSession,
        offset: int = 0,
        page: int = 10,
        fuel_type: str | None = None,
        depot: str | None = None,
        region: str | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ) -> bool | None:
        stmt = (
            select(OrderPublic)
            .where(
                (user.is_admin | OrderPublic.user.id == user.id)
                & (OrderPublic.lot.fuel == fuel_type if fuel_type else true())
                & (OrderPublic.lot.depot == depot if depot else true())
                & (OrderPublic.lot.region == region if region else true())
                & (OrderPublic.status == status if status else true())
                & (
                    OrderPublic.user.id == user_id
                    if user_id and user.is_admin
                    else True
                ),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )
        return await session.scalar(stmt)

    @staticmethod
    async def get_order_by_id(
        user: UserDep,
        session: AsyncSession,
        order_id: int,
    ) -> bool | None:
        stmt = select(
            exists().where(col(OrderPublic.id) == order_id)
            & (user.is_admin | OrderPublic.user.id == user.id),
        )
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
