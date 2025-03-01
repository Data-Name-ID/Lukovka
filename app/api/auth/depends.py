from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

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
