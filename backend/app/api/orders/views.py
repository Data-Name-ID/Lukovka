from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Query
from starlette import status

from api.auth.depends import AdminDep, SessionDep, UserDep
from api.orders import errors
from api.orders.filters import OrderFilterParams
from core.models.orders import OrderCreate, OrderPublic, OrderUpdate, OrderWithPages
from core.schemas import DetailScheme, MessageScheme
from core.store import store

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get(
    "",
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

    if order is None:
        raise errors.ORDER_NOT_FOUND

    return OrderPublic(
        **order.model_dump(exclude={"depot", "fuel"}),
        depot=order.lot.depot.name,
        fuel=order.lot.fuel.name,
        region=order.lot.depot.region,
    )


@router.post(
    "",
    summary="Создание заказ",
    response_description="Создание заказа",
)
async def order_create(
    order_in: OrderCreate,
    background_tasks: BackgroundTasks,
    user: UserDep,
    session: SessionDep,
) -> int:
    order_id = await store.order_manager.process_creating_order(
        session=session,
        user_id=user.id,
        order_in=order_in,
    )

    background_tasks.add_task(
        store.order_manager.send_create_order_email,
        user=user,
        order_id=order_id,
    )

    return order_id


@router.patch(
    "/{order_id}/status",
    summary="Изменение статуса заказа",
    response_description="Изменение статуса заказа",
)
async def change_status_order(
    order_in: OrderUpdate,
    user: AdminDep,
    session: SessionDep,
    background_tasks: BackgroundTasks,
    order_id: int,
) -> OrderPublic:
    res, old_status, new_status = await store.order_manager.change_status_order(
        session=session,
        order_id=order_id,
        order_in=order_in,
        user=user,
    )

    background_tasks.add_task(
        store.order_manager.send_info_email,
        user=user,
        old_status=old_status,
        new_status=new_status,
        order_id=order_id,
    )

    return res


@router.patch(
    "/{order_id}/cancel",
    summary="Отмена заказа",
    response_description="Отмена заказа",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Заказ с id {order_id} не найден",
            "model": DetailScheme,
        },
    },
)
async def order_cancel(
    order_id: int,
    user: UserDep,
    session: SessionDep,
) -> MessageScheme:
    await store.order_manager.process_canceling_order(
        session=session,
        user=user,
        order_id=order_id,
    )
    return MessageScheme(message="Заказ успешно отменен")
