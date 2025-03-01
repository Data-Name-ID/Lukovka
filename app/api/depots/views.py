from fastapi import APIRouter

from api.auth.depends import AdminDep, SessionDep, UserDep
from core.models.depots import (
    DepotNamePublic,
    DepotPublic,
    DepotRegionPublic,
)
from core.store import store

router = APIRouter(prefix="/depots", tags=["Depots"])


@router.get(
    "/names",
    summary="Имена нефтебаз",
    response_description="Имена нефтебаз",
)
async def get_depots_names(
    _user: UserDep,
    session: SessionDep,
) -> list[DepotNamePublic]:
    depots = await store.depons_accessor.get_depots_names(
        session=session,
    )
    return depots


@router.get(
    "/regions",
    summary="Регионы нефтебаз",
    response_description="Регионы нефтебаз",
)
async def get_depots_regions(
    _user: UserDep,
    session: SessionDep,
) -> list[DepotRegionPublic]:
    depots = await store.depons_accessor.get_depots_regions(
        session=session,
    )
    return depots


@router.post(
    "/",
    summary="Добавление нефтебазы",
    response_description="Добавление нефтебазы",
)
async def depot_create(
    _user: AdminDep,
    depot_in: DepotPublic,
    session: SessionDep,
) -> None:
    return await store.depons_accessor.create_depot(
        session=session,
        depot_in=depot_in,
    )


# @router.get(
#     "/{lot_id}",
#     summary="Лот по ID",
#     response_description="Лот",
# )
# async def get_lots_by_id(
#     _user: UserDep,
#     session: SessionDep,
#     lot_id: int,
# ) -> LotDetail | None:
#     lot = await store.lot_accessor.get_lot_by_id(
#         session=session,
#         lot_id=lot_id,
#     )
#     return LotDetail(
#         **lot.model_dump(exclude={"depot", "fuel"}),
#         depot=lot.depot.name,
#         fuel=lot.fuel.name,
#         region=lot.depot.region,
#     )
