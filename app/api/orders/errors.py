from fastapi import HTTPException
from starlette import status

NOT_ENOUGH_FUEL = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Недостаточно топлива",
)

FUEL_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Не найдено",
)

ORDER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Не найдено",
)
