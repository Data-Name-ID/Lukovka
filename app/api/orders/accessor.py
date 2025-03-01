from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import col, exists, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.user import User, UserCreate
from core.store import Store


class OrderAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def get_all_orders(
        *,
        session: AsyncSession,
        offset: int = 0,
        page: int = 10,
        fuel_type: str | None = None,
        depot: str | None = None,
    ) -> bool | None:
        stmt = ...
        return await session.scalar(stmt)

    @staticmethod
    async def get_order_by_id(session: AsyncSession, order_id: int) -> bool | None:
        stmt = ...
        return await session.scalar(stmt)

    @staticmethod
    async def create_order(*, user_in: UserCreate, session: AsyncSession) -> int:
        # TODO: проверить доступное количество топлива перед созданием
        stmt = ...
        return await session.scalar(stmt)
