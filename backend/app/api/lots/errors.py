from fastapi import HTTPException
from starlette import status

INVALID_FILE_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка обработки файла, проверьте его корректность",
)
