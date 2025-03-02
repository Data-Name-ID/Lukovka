from fastapi import APIRouter

from api.auth.depends import AdminDep, SessionDep, UserDep
from core.models.fuels import FuelPublic
from core.store import store

router = APIRouter(prefix="/fuels", tags=["Fuels"])


@router.get(
    "/types",
    summary="Типы топлива",
    response_description="Типы топлива",
)
async def get_fuels_names(
    _user: UserDep,
    session: SessionDep,
) -> list[FuelPublic]:
    return await store.fuels_accessor.get_fuels_names(
        session=session,
    )


@router.post(
    "",
    summary="Добавление топлива",
    response_description="Добавление топлива",
)
async def depot_create(
    _user: AdminDep,
    fuel_in: FuelPublic,
    session: SessionDep,
) -> None:
    return await store.fuels_accessor.create_fuel(
        session=session,
        fuel_in=fuel_in,
    )
