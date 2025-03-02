from fastapi import HTTPException
from starlette import status

NOT_ENOUGH_FUEL = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Недостаточно топлива",
)

FUEL_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Топливо не найдено",
)

ORDER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Заказ не найден",
)

ORDER_ALREADY_CANCELED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Заказ уже был отменён",
)
