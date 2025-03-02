from fastapi import HTTPException
from starlette import status

INVALID_TOKEN_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Недействительный токен",
)
UNACTIVATED_USER_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не активирован",
)
USER_ALREADY_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)
USER_NOT_EXISTS = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователя не существует",
)
USER_NOT_ADMIN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав",
)
