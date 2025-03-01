from fastapi import APIRouter

from api.auth.depends import SessionDep, UserDep
from core.models.lots import LotWithPages
from core.store import store

router = APIRouter(prefix="/lots", tags=["Lots"])


@router.get(
    "",
    summary="Лоты",
    response_description="Лоты",
)
async def get_lots(
    # _user: UserDep,
    session: SessionDep,
    page: int | None = 1,
    offset: int | None = 10,
    fuel_type: str | None = None,
    depot: str | None = None,
    region: str | None = None,
) -> LotWithPages:
    page_count, lots = await store.lots_accessor.get_all_lots(
        page=page,
        offset=offset,
        fuel_type=fuel_type,
        depot=depot,
        region=region,
        session=session,
    )
    return LotWithPages(
        page_count=page_count,
        lots=lots,
    )


@router.get(
    "/{lot_id}",
    summary="Лот по ID",
    response_description="Лот",
)
async def get_lots_by_id(
    _user: UserDep,
    session: SessionDep,
    lot_id: int,
) -> None:
    return await store.lots_accessor.get_lots_by_id(
        session=session,
        lot_id=lot_id,
    )
