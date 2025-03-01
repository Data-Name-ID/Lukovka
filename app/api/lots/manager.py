import io
from csv import DictReader
from typing import BinaryIO

from sqlmodel.ext.asyncio.session import AsyncSession

from core.models.lots import LotCreate
from core.store import Store


class LotManager:
    def __init__(self, store: Store) -> None:
        self.store = store

    async def create_lots_from_csv(
        self,
        *,
        csv_file: BinaryIO,
        session: AsyncSession,
    ) -> None:
        reader = DictReader(io.TextIOWrapper(csv_file, encoding="utf-8"))
        lots = [
            LotCreate(**row)
            for row in reader
            if all(val.strip() for val in row.values())
        ]
        await self.store.lot_accessor.create_lots(lots=lots, session=session)
        await session.commit()
