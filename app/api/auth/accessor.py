from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from sqlmodel import col, exists, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.user import User, UserCreate
from core.store import Store


class UserAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    async def create_user(*, user_in: UserCreate, session: AsyncSession) -> int:
        stmt = (
            insert(User)
            .values(
                **user_in.model_dump(exclude={"password"}),
                password=UserCreate.hash_password(user_in.password),
            )
            .returning(col(User.id))
        )
        return await session.scalar(stmt)

    @staticmethod
    async def user_exists_by_id(*, user_id: int, session: AsyncSession) -> bool | None:
        stmt = select(exists().where(col(User.id) == user_id))
        return await session.scalar(stmt)

    @staticmethod
    async def user_exists_by_email(*, email: str, session: AsyncSession) -> bool | None:
        stmt = select(exists().where(col(User.email) == email))
        return await session.scalar(stmt)

    @staticmethod
    async def fetch_user_by_id(*, user_id: int, session: AsyncSession) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(load_only(User.id, User.activated, User.email))  # type: ignore[arg-type]
        )
        return await session.scalar(stmt)

    @staticmethod
    async def fetch_user_by_email(*, email: str, session: AsyncSession) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
            .options(load_only(User.id, User.password))  # type: ignore[arg-type]
        )
        return await session.scalar(stmt)

    @staticmethod
    async def activate_user(
        *,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        stmt = update(User).where(col(User.id) == user_id).values(activated=True)
        await session.exec(stmt)
        await session.commit()
