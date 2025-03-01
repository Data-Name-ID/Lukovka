from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette import status

from api.auth import errors
from api.auth.depends import SessionDep, UserDep
from app.core.models.orders import OrderCreate
from core.models.jwt import AccessToken, RefreshToken, TokenCollection
from core.models.user import UserCreate, UserLogin, UserPublic
from core.schemas import DetailScheme
from core.store import store

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get(
    "/",
    summary="Заказы",
    response_description="Заказы пользователя",
)
async def get_orders(
    user: UserDep,
    session: SessionDep,
    offset: int = 1,
    page: int = 10,
    fuel_type: str | None = None,
    depot: str | None = None,
    region: str | None = None,
):
    return await store.order_accessor.get_all_orders(
        session=session,
        offset=offset,
        page=page,
        fuel_type=fuel_type,
        depot=depot,
        region=region,
    )


@router.get(
    "/{order_id}",
    summary="Заказ",
    response_description="Заказ",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Заказ с id {order_id} не найден",
            "model": DetailScheme,
        },
    },
)
async def get_order_by_id(user: UserDep) -> UserPublic:
    return store.order_accessor.get_order_by_id(user_id=user.id)


@router.post(
    "/",
    summary="Создание заказ",
    response_description="Создание заказа",
)
async def order_create(
    user: UserDep,
    order_in: OrderCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    session: SessionDep,
) -> int:
    order_id = await store.order_accessor.create_order(
        session=session,
        user_id=user.id,
        order_in=order_in,
    )
    await session.commit()

    return order_id
