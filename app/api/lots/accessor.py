from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.lots import Lot
from core.store import Store


class LotsAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_lots(
        *,
        session: AsyncSession,
        page: int | None = 1,
        offset: int | None = 10,
        fuel_type: str | None = None,
        depot: str | None = None,
        region: str | None = None,
) -> list[Lot]:
        stmt = (
            select(Lot)
            .where(
                (Lot.fuel == fuel_type if fuel_type else True) &
                (Lot.depot == depot if depot else True) &
                (Lot.region == region if region else True),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )
        return list((await session.scalars(stmt)).all())

    @staticmethod
    async def get_lots_by_id(
        session: AsyncSession,
        lot_id: int,
    ) -> Lot:
        stmt = ...
        return await session.scalar(stmt)
