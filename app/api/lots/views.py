from typing import Annotated

from fastapi import APIRouter, Query, UploadFile

from api.auth.depends import AdminDep, SessionDep, UserDep
from api.lots import errors
from api.lots.filters import LotFilterParams
from core.models.lots import LotDetail, LotPublic, LotWithPages
from core.store import store

router = APIRouter(prefix="/lots", tags=["Lots"])


@router.get(
    "",
    summary="Лоты",
    response_description="Лоты",
)
async def get_lots(
    filter_query: Annotated[LotFilterParams, Query()],
    user: UserDep,
    session: SessionDep,
) -> LotWithPages:
    page_count, lots = await store.lot_accessor.get_lots(
        filter_query=filter_query,
        user=user,
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
) -> LotDetail | None:
    lot = await store.lot_accessor.get_lot_by_id(
        session=session,
        lot_id=lot_id,
    )
    return LotDetail(
        **lot.model_dump(exclude={"depot", "fuel"}),
        depot=lot.depot.name,
        fuel=lot.fuel.name,
        region=lot.depot.region,
    )


@router.post("/upload")
async def create_upload_file(
    csv_file: UploadFile,
    _user: AdminDep,
    session: SessionDep,
) -> int:
    try:
        return await store.lot_manager.create_lots_from_csv(
            csv_file=csv_file.file,
            session=session,
        )
    except Exception as e:
        raise errors.INVALID_FILE_ERROR from e
