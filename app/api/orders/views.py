from typing import Annotated

from fastapi import APIRouter, Query
from starlette import status

from api.auth.depends import SessionDep, UserDep
from api.orders.filters import OrderFilterParams
from core.models.orders import OrderCreate, OrderPublic, OrderWithPages
from core.schemas import DetailScheme
from core.store import store

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get(
    "/",
    summary="Заказы",
    response_description="Заказы пользователя",
)
async def get_orders(
    filter_query: Annotated[OrderFilterParams, Query()],
    user: UserDep,
    session: SessionDep,
) -> OrderWithPages:
    page_count, orders = await store.order_accessor.get_orders(
        filter_query=filter_query,
        user=user,
        session=session,
    )
    return OrderWithPages(
        page_count=page_count,
        orders=[
            OrderPublic(
                **order.model_dump(exclude={"depot", "fuel"}),
                depot=order.lot.depot.name,
                fuel=order.lot.fuel.name,
                region=order.lot.depot.region,
            )
            for order in orders
        ],
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
async def get_order_by_id(
    order_id: int,
    user: UserDep,
    session: SessionDep,
) -> OrderPublic:
    order = await store.order_accessor.get_order_by_id(
        user=user,
        order_id=order_id,
        session=session,
    )
    return OrderPublic(
        **order.model_dump(exclude={"depot", "fuel"}),
        depot=order.lot.depot.name,
        fuel=order.lot.fuel.name,
        region=order.lot.depot.region,
    )


@router.post(
    "/",
    summary="Создание заказ",
    response_description="Создание заказа",
)
async def order_create(
    order_in: OrderCreate,
    user: UserDep,
    session: SessionDep,
) -> int:
    return await store.order_manager.process_creating_order(
        session=session,
        user_id=user.id,
        order_in=order_in,
    )
