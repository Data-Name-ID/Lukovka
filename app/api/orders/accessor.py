from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlmodel import col, exists, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.lots import Lot
from core.models.orders import Order, OrderCreate, OrderPublic
from core.models.user import User
from core.store import Store


class OrderAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_orders(
        *,
        user: User,
        session: AsyncSession,
        offset: int = 0,
        page: int = 10,
        fuel_type: str | None = None,
        depot: str | None = None,
        region: str | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ) -> list[Order]:
        stmt = select(Order).join(Lot, Order.lot_id == Lot.id)

        if not user.is_admin:
            stmt = stmt.where(Order.user_id == user.id)

        if fuel_type:
            stmt = stmt.where(Order.lot.fuel == fuel_type)
        if depot:
            stmt = stmt.where(Order.lot.depot == depot)
        if region:
            stmt = stmt.where(Order.lot.depot.region == region)
        if status:
            stmt = stmt.where(Order.status == status)
        if user_id and user.is_admin:
            stmt = stmt.where(Order.user_id == user_id)

        stmt = (
            stmt.options(selectinload(Order.lot))
            .offset((page - 1) * offset)
            .limit(offset)
        )

        return (await session.scalars(stmt)).all()

    @staticmethod
    async def get_order_by_id(
        user: User,
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
