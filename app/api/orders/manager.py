from sqlmodel.ext.asyncio.session import AsyncSession

from api.orders import errors
from core.models.orders import OrderCreate
from core.store import Store


class OrderManager:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def process_creating_order(
        self,
        *,
        user_id: int,
        order_in: OrderCreate,
        session: AsyncSession,
    ) -> int:
        lot = await self.store.lot_accessor.get_lot_by_id(
            lot_id=order_in.lot_id, session=session,
        )

        if not lot:
            raise errors.FUEL_NOT_FOUND

        if lot.current_volume < order_in.volume:
            raise errors.NOT_ENOUGH_FUEL

        lot.current_volume -= order_in.volume
        order = await self.store.order_accessor.create_order(
            user_id=user_id,
            order_in=order_in,
            session=session,
        )
        await session.commit()
        return order
