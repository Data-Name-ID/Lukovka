from fastapi import APIRouter, UploadFile

from api.auth.depends import SessionDep, UserDep
from core.models.lots import LotPublic, LotWithPages
from core.store import store

router = APIRouter(prefix="/lots", tags=["Lots"])


@router.post("/upload")
async def create_upload_file(csv_file: UploadFile):
    return await store.lot_manager.create_lots_from_csv(csv_file=csv_file.file)


@router.get(
    "",
    summary="Лоты",
    response_description="Лоты",
)
async def get_lots(
    # _user: UserDep,
    session: SessionDep,
    page: int = 1,
    offset: int = 10,
    fuel: str | None = None,
    depot: str | None = None,
    region: str | None = None,
) -> LotWithPages:
    page_count, lots = await store.lot_accessor.get_all_lots(
        page=page,
        offset=offset,
        fuel=fuel,
        depot=depot,
        region=region,
        session=session,
    )
    return LotWithPages(
        page_count=page_count,
        lots=[
            LotPublic(
                **lot.model_dump(exclude={"depot", "fuel"}),
                depot=lot.depot.name,
                fuel=lot.fuel.name,
                region=lot.depot.region,
            )
            for lot in lots
        ],
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
) -> LotPublic | None:
    return await store.lot_accessor.get_lot_by_id(
        session=session,
        lot_id=lot_id,
    )
