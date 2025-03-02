from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.lots.filters import LotFilterParams
from core.models.depots import Depot
from core.models.fuels import Fuel
from core.models.lots import Lot, LotStatusEnum
from core.models.user import User
from core.store import Store


class LotsAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def get_lots(
        self,
        *,
        filter_query: LotFilterParams,
        user: User,
        session: AsyncSession,
    ) -> tuple[int, list[Lot]]:
        mapping = {
            "fuel": Fuel.name,
            "depot": Depot.name,
            "region": Depot.region,
        }

        conditions = [
            self.store.core_accessor.make_condition(getattr(filter_query, key), column)
            for key, column in mapping.items()
        ]
        conditions = [cond for cond in conditions if cond is not None]

        if not user.is_admin:
            conditions.append(Lot.status == LotStatusEnum.CONFIRMED.value)

        query = (
            select(Lot, func.count(Lot.id).over().label("total_count"))
            .join(Fuel, Fuel.id == Lot.fuel_id)
            .join(Depot, Depot.id == Lot.depot_id)
            .options(selectinload(Lot.fuel), selectinload(Lot.depot))
            .where(*conditions)
            .offset((filter_query.page - 1) * filter_query.offset)
            .limit(filter_query.offset)
        )

        result = await session.exec(query)
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
    async def get_lot_by_id(lot_id: int, session: AsyncSession) -> Lot | None:
        stmt = (
            select(Lot)
            .where(Lot.id == lot_id)
            .options(selectinload(Lot.fuel), selectinload(Lot.depot))
        )
        return await session.scalar(stmt)

    @staticmethod
    async def create_lots(
        lots: list[dict[str, Any], None, None],
        session: AsyncSession,
    ) -> Lot | None:
        stmt = insert(Lot).values(lots).returning(Lot)
        await session.exec(stmt)
        await session.commit()
