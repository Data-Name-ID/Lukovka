from typing import TYPE_CHECKING

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlmodel import VARCHAR, BigInteger, Column, Field, Relationship

from core.db import BaseSQLModel

if TYPE_CHECKING:
    from core.models.orders import Order

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseSQLModel):
    email: EmailStr = Field(
        sa_column=Column(VARCHAR(254), unique=True, index=True, nullable=False),
    )


class ConfirmMixin(BaseSQLModel):
    activated: bool = False


class UserCreate(UserBase):
    password: str = Field(sa_column=Column(VARCHAR(1024), nullable=False))

    def validate_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


class User(UserCreate, ConfirmMixin, table=True):
    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True),
    )

    orders: list["Order"] = Relationship(back_populates="lot")


class UserPublic(UserBase):
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserEmailUpdate(BaseModel):
    email: EmailStr


class UserPasswordUpdate(BaseModel):
    password: str
