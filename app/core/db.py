from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import MetaData, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

if TYPE_CHECKING:
    from core.store import Store


class BaseSQLModel(SQLModel):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": ("fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"),
            "pk": "pk_%(table_name)s",
        },
    )


class DatabaseAccessor:
    def __init__(self, store: "Store") -> None:
        self.store = store
        self.engine: AsyncEngine = create_async_engine(
            url=store.config.db.url,
            echo=store.config.db.echo,
            echo_pool=store.config.db.echo_pool,
            pool_size=store.config.db.pool_size,
            max_overflow=store.config.db.max_overflow,
        )

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(self.engine) as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()
