from sqlmodel import func, select
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
) -> tuple[int, list[Lot]]:
        stmt = (
            select(
                Lot,
                func.count().over().label("total_count"),
            )
            .where(
                (Lot.fuel == fuel_type if fuel_type else True) &
                (Lot.depot == depot if depot else True) &
                (Lot.region == region if region else True),
            )
            .offset((page - 1) * offset)
            .limit(offset)
        )
        results = (await session.scalars(stmt)).all()
        lots_count = results[0][1] if results else 0
        page_count = (lots_count + offset - 1) // offset
        return page_count, [elem[0] for elem in results]
