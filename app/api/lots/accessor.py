from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col, func, select
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
        stmt = (
            select(
                Lot,
                func.count().over().label("total_count"),
            )
            .join(Fuel, col(Fuel.id) == col(Lot.fuel_id))
            .join(Depot, col(Depot.id) == col(Lot.depot_id))
            .where(
                (Fuel.name == fuel if fuel else True)
                & (Depot.name == depot if depot else True)
                & (Depot.region == region if region else True),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )
        results = (await session.scalars(stmt)).all()
        lots_count = results[0][1] if results else 0
        page_count = (lots_count + offset - 1) // offset
        return page_count, [elem[0] for elem in results]

    @staticmethod
    async def get_lot_by_id(lot_id: int, session: AsyncSession) -> Lot | None:
        stmt = select(Lot).where(Lot.id == lot_id)
        return await session.scalar(stmt)

    @staticmethod
    async def create_lots(lots: list[LotCreate], session: AsyncSession) -> Lot | None:
        stmt = (
            insert(Lot)
            .values(
                [lot.model_dump() for lot in lots],
            )
            .returning(Lot)
        )
        return await session.scalar(stmt)
