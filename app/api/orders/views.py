from fastapi import APIRouter, Request
from starlette import status

from api.auth.depends import SessionDep, UserDep
from api.orders import manager
from core.models.orders import OrderCreate, OrderId, OrderPublic
from core.models.user import UserPublic
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
    status: str | None = None,
    user_id: int | None = None,
) -> list[OrderPublic]:
    return await store.order_accessor.get_all_orders(
        user=user,
        session=session,
        offset=offset,
        page=page,
        fuel_type=fuel_type,
        depot=depot,
        region=region,
        status=status,
        user_id=user_id,
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
    return store.order_accessor.get_order_by_id(user=user)


@router.post(
    "/",
    summary="Создание заказ",
    response_description="Создание заказа",
)
async def order_create(
    user: UserDep,
    order_in: OrderCreate,
    request: Request,
    session: SessionDep,
) -> OrderId:
    order_id = manager.process_creating_order(
        session=session,
        lot_id=order_in.lot_id,
        request_quantity=order_in.volume,
    )

    return OrderId(order_id=order_id)
