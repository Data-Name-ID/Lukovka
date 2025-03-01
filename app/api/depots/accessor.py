from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.depots import Depot, DepotPublic
from core.store import Store


class DepotsAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_depots_names(
        *,
        session: AsyncSession,
    ) -> list[Depot]:
        stmt = select(Depot).options(load_only(Depot.id, Depot.name))

        return await session.scalars(stmt)

    @staticmethod
    async def get_depots_regions(
        *,
        session: AsyncSession,
    ) -> list[Depot]:
        stmt = select(Depot).options(load_only(Depot.id, Depot.region))

        return await session.scalars(stmt)

    @staticmethod
    async def create_depot(
        *,
        depot_in: DepotPublic,
        session: AsyncSession,
    ) -> Depot:
        stmt = insert(Depot).values(**depot_in.model_dump()).returning(Depot)
        await session.scalar(stmt)
        await session.commit()
        return None

    # @staticmethod
    # async def get_lot_by_id(lot_id: int, session: AsyncSession) -> Lot | None:
    #     stmt = (
    #         select(Lot)
    #         .where(Lot.id == lot_id)
    #         .options(selectinload(Lot.fuel), selectinload(Lot.depot))
    #     )
    #     return await session.scalar(stmt)

    # @staticmethod
    # async def create_lots(
    #     lots: list[dict[str, Any], None, None],
    #     session: AsyncSession,
    # ) -> Lot | None:
    #     stmt = insert(Lot).values(lots).returning(Lot)
    #     return await session.exec(stmt)
