from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from api.auth import errors
from core.models.user import User
from core.store import store

bearer_scheme = HTTPBearer()

TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
SessionDep = Annotated[AsyncSession, Depends(store.db.session)]


async def user_dependency(token: TokenDep, session: SessionDep) -> User:
    return await store.user_manager.fetch_user_from_access_token(
        session=session,
        token=token.credentials,
    )


UserDep = Annotated[User, Depends(user_dependency)]


def admin_dependency(user: UserDep) -> User:
    if not user.is_admin:
        raise errors.USER_NOT_ADMIN

    return user


AdminDep = Annotated[User, Depends(admin_dependency)]
