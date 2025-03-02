from fastapi import APIRouter

from core.models.ping import PingPublic

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get(
    "",
    summary="Проверка ответа севера",
    response_description="Успешный ответ",
)
async def ping() -> PingPublic:
    return PingPublic()
