from fastapi import APIRouter

from api.auth.depends import AdminDep, SessionDep, UserDep
from core.models.fuels import (
    FuelPublic,
    # DepotPublic,
    # DepotRegionPublic,
)
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
    fuels = await store.fuels_accessor.get_fuels_names(
        session=session,
    )
    return fuels


# @router.get(
#     "/regions",
#     summary="Регионы нефтебаз",
#     response_description="Регионы нефтебаз",
# )
# async def get_depots_regions(
#     _user: UserDep,
#     session: SessionDep,
# ) -> list[DepotRegionPublic]:
#     depots = await store.depons_accessor.get_depots_regions(
#         session=session,
#     )
#     return depots
#
#
# @router.post(
#     "/",
#     summary="Добавление нефтебазы",
#     response_description="Добавление нефтебазы",
# )
# async def depot_create(
#     _user: AdminDep,
#     depot_in: DepotPublic,
#     session: SessionDep,
# ) -> None:
#     return await store.depons_accessor.create_depot(
#         session=session,
#         depot_in=depot_in,
#     )
