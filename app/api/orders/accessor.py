from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlmodel import col, exists, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.orders.filters import OrderFilterParams
from core.models.depots import Depot
from core.models.fuels import Fuel
from core.models.lots import Lot
from core.models.orders import Order, OrderCreate, OrderPublic
from core.models.user import User
from core.store import Store


class OrderAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def get_orders(
        self,
        *,
        filter_query: OrderFilterParams,
        user: User,
        session: AsyncSession,
    ) -> tuple[int, list[Order]]:
        mapping = {
            "fuel": Fuel.name,
            "depot": Depot.name,
            "region": Depot.region,
            "status": Order.status,
        }

        conditions = [
            self.store.core_accessor.make_condition(getattr(filter_query, key), column)
            for key, column in mapping.items()
        ]
        conditions = [cond for cond in conditions if cond is not None]

        if not user.is_admin:
            conditions.append(Order.user_id == user.id)
        elif getattr(filter_query, "user_id", None):
            conditions.append(Order.user_id == filter_query.user_id)

        query = (
            select(Order, func.count(Order.id).over().label("total_count"))
            .join(Lot, Order.lot_id == Lot.id)
            .join(Fuel, Fuel.id == Lot.fuel_id)
            .join(Depot, Depot.id == Lot.depot_id)
            .options(
                selectinload(Order.lot).selectinload(Lot.depot),
                selectinload(Order.lot).selectinload(Lot.fuel),
            )
            .where(*conditions)
            .offset((filter_query.page - 1) * filter_query.offset)
            .limit(filter_query.offset)
        )

        result = await session.execute(query)
        rows = result.all()

        if rows:
            total_count = rows[0][1]
            data = [row[0] for row in rows]
        else:
            total_count = 0
            data = []

        page_count = (
            (total_count + filter_query.offset - 1) // filter_query.offset
            if filter_query.offset
            else 0
        )
        return page_count, data

    @staticmethod
    async def get_order_by_id(
        *,
        order_id: int,
        user: User,
        session: AsyncSession,
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
            .values(**order_in.model_dump(), user_id=user_id)
            .returning(Order)
        )
        return await session.scalar(stmt)
