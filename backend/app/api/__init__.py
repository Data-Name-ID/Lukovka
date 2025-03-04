from fastapi import APIRouter

from api.auth.views import router as auth_router
from api.depots.views import router as depots_router
from api.fuels.views import router as fuels_router
from api.lots.views import router as lots_router
from api.orders.views import router as orders_router
from api.ping.views import router as ping_router

router = APIRouter(prefix="/api")

router.include_router(ping_router)
router.include_router(auth_router)
router.include_router(lots_router)
router.include_router(orders_router)
router.include_router(depots_router)
router.include_router(fuels_router)
