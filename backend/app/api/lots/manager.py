import io
from csv import DictReader
from typing import BinaryIO

from pydantic import ValidationError
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
        lots = []

        text_stream = io.TextIOWrapper(csv_file, encoding="utf-8")
        reader = DictReader(text_stream)

        for row in reader:
            if not all(val.strip() for val in row.values()):
                continue

            try:
                lot_data = LotCreate.model_validate(row).model_dump()
            except ValidationError:
                continue

            lots.append(lot_data)

        if lots:
            await self.store.lot_accessor.create_lots(lots=lots, session=session)

        return len(lots)
