from jwt import InvalidTokenError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.datastructures import URL

from api.auth import errors
from core.models.jwt import AccessToken, TokenPayload, TokenType
from core.models.user import User, UserCreate
from core.store import Store


class UserManager:
    def __init__(self, store: Store) -> None:
        self.store = store

    def extract_payload_from_token(
        self,
        *,
        token: str,
        token_type: TokenType,
    ) -> TokenPayload:
        try:
            payload = self.store.jwt.decode_jwt(token)
        except InvalidTokenError as e:
            raise errors.INVALID_TOKEN_ERROR from e

        if payload.typ != token_type.value:
            raise errors.INVALID_TOKEN_ERROR

        return payload

    async def fetch_user_from_access_token(
        self,
        *,
        token: str,
        session: AsyncSession,
    ) -> User:
        payload = self.extract_payload_from_token(
            token=token,
            token_type=TokenType.ACCESS,
        )

        user = await self.store.user_accessor.fetch_user_by_id(
            user_id=int(payload.sub),
            session=session,
        )

        if not user:
            raise errors.INVALID_TOKEN_ERROR

        if not user.activated:
            raise errors.UNACTIVATED_USER_ERROR

        return user

    async def refresh_access_token(
        self,
        *,
        token: str,
        session: AsyncSession,
    ) -> AccessToken:
        payload = self.extract_payload_from_token(
            token=token,
            token_type=TokenType.REFRESH,
        )
        user_id = int(payload.sub)

        if not self.store.user_accessor.user_exists_by_id(
            user_id=user_id,
            session=session,
        ):
            raise errors.USER_NOT_EXISTS

        token = self.store.jwt.create_access_token(user_id, payload.jti).token
        return AccessToken(access_token=token)

    async def activate_user_by_token(
        self,
        *,
        token: str,
        session: AsyncSession,
    ) -> None:
        payload = self.extract_payload_from_token(
            token=token,
            token_type=TokenType.EMAIL_CONFIRM,
        )

        await self.store.user_accessor.activate_user(
            user_id=int(payload.sub),
            session=session,
        )

    async def send_confirm_email(
        self,
        *,
        user_id: int,
        user: UserCreate,
        base_url: str | URL,
    ) -> None:
        token = self.store.jwt.create_email_confirm_token(user_id).token
        await self.store.email.send_email(
            recipient=user.email,
            title="Подтверждение аккаунта",
            template="email_confirm.html",
            base_url=base_url,
            url=f"{base_url}api/auth/confirm-email?token={token}",
        )
