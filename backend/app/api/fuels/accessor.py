from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.fuels import Fuel, FuelPublic
from core.store import Store


class FuelsAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_fuels_names(
        *,
        session: AsyncSession,
    ) -> list[Fuel]:
        stmt = select(Fuel).options(load_only(Fuel.id, Fuel.name))

        return await session.scalars(stmt)

    @staticmethod
    async def create_fuel(
        *,
        fuel_in: FuelPublic,
        session: AsyncSession,
    ) -> None:
        stmt = insert(Fuel).values(**fuel_in.model_dump()).returning(Fuel)
        await session.scalar(stmt)
        await session.commit()
