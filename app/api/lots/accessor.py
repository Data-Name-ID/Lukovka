from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col, func, select, true
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.depots import Depot
from core.models.fuels import Fuel
from core.models.lots import Lot, LotCreate
from core.store import Store


class LotsAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_lots(
        *,
        session: AsyncSession,
        page: int = 1,
        offset: int = 10,
        fuel: str | None = None,
        depot: str | None = None,
        region: str | None = None,
    ) -> tuple[int, list[Lot]]:
        data_stmt = (
            select(Lot)
            .join(Fuel, Fuel.id == Lot.fuel_id)
            .join(Depot, Depot.id == Lot.depot_id)
            .options(selectinload(Lot.fuel), selectinload(Lot.depot))
            .where(
                (Fuel.name == fuel if fuel else true()),
                (Depot.name == depot if depot else true()),
                (Depot.region == region if region else true()),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )

        count_stmt = (
            select(func.count(Lot.id))
            .join(Fuel, Fuel.id == Lot.fuel_id)
            .join(Depot, Depot.id == Lot.depot_id)
            .where(
                (Fuel.name == fuel if fuel else true()),
                (Depot.name == depot if depot else true()),
                (Depot.region == region if region else true()),
            )
        )
        total_count = await session.scalar(count_stmt)

        data = (await session.scalars(data_stmt)).all()
        page_count = (total_count + offset - 1) // offset
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
    async def create_lots(lots: list[LotCreate], session: AsyncSession) -> Lot | None:
        stmt = (
            insert(Lot)
            .values(
                [{**lot.model_dump()} for lot in lots],
            )
            .returning(Lot)
        )
        return await session.scalar(stmt)
