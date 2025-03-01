from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from core.models.jwt import (
    Token,
    TokenCollection,
    TokenPayload,
    TokenType,
)
from core.store import Store


class JWTManager:
    def __init__(self, store: Store) -> None:
        self.private_key = store.config.jwt.private_key_path.read_bytes()
        self.public_key = store.config.jwt.public_key_path.read_bytes()
        self.algorithm = store.config.jwt.algorithm
        self.access_token_expiration_minutes = (
            store.config.jwt.access_token_expiration_minutes
        )
        self.refresh_token_expiration_minutes = (
            store.config.jwt.refresh_token_expiration_days * 24 * 60
        )
        self.email_confirm_expiration_minutes = 60 * 24
        self.reset_password_expiration_minutes = 60

    def encode_jwt(
        self,
        user_id: int,
        token_type: TokenType,
        expire_minutes: int,
        rjti: str | None = None,
    ) -> Token:
        now = datetime.now(tz=UTC)
        exp = now + timedelta(minutes=expire_minutes)
        jti = uuid4().hex

        payload = TokenPayload(
            typ=token_type,
            jti=jti,
            iat=now.timestamp(),
            exp=exp.timestamp(),
            sub=str(user_id),
            rjti=rjti,
        ).model_dump(exclude_none=True)

        token = jwt.encode(
            payload,
            key=self.private_key,
            algorithm=self.algorithm,
        )
        return Token(token=token, jti=jti)

    def decode_jwt(self, token: str | bytes) -> TokenPayload:
        payload = jwt.decode(
            jwt=token,
            key=self.public_key,
            algorithms=[self.algorithm],
        )
        return TokenPayload(**payload)

    def create_token_collection(self, user_id: int) -> TokenCollection:
        refresh_token = self.create_refresh_token(user_id)
        access_token = self.create_access_token(user_id, refresh_token.jti)

        return TokenCollection(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

    def create_access_token(
        self,
        user_id: int,
        rjti: str | None = None,
    ) -> Token:
        return self.encode_jwt(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            expire_minutes=self.access_token_expiration_minutes,
            rjti=rjti,
        )

    def create_refresh_token(self, user_id: int) -> Token:
        return self.encode_jwt(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            expire_minutes=self.refresh_token_expiration_minutes,
        )

    def create_email_confirm_token(self, user_id: int) -> Token:
        return self.encode_jwt(
            user_id=user_id,
            token_type=TokenType.EMAIL_CONFIRM,
            expire_minutes=self.email_confirm_expiration_minutes,
        )

    def create_password_reset_token(self, user_id: int) -> Token:
        return self.encode_jwt(
            user_id=user_id,
            token_type=TokenType.RESET_PASSWORD,
            expire_minutes=self.reset_password_expiration_minutes,
        )
