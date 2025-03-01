import logging


class Store:
    def __init__(self) -> None:
        from core.config import Config

        self.config = Config()

        from core.email import EmailManager
        from core.jwt import JWTManager

        self.email = EmailManager(self)
        self.jwt = JWTManager(self)

        from core.db import DatabaseAccessor

        self.db = DatabaseAccessor(self)

        from api.auth.accessor import UserAccessor
        from api.depots.accessor import DepotsAccessor
        from api.lots.accessor import LotsAccessor
        from api.orders.accessor import OrderAccessor
        from core.accessor import CoreAccessor

        self.user_accessor = UserAccessor(self)

        self.order_accessor = OrderAccessor(self)
        self.lot_accessor = LotsAccessor(self)
        self.depots_accessor = DepotsAccessor(self)
        self.core_accessor = CoreAccessor(self)

        from api.auth.manager import UserManager
        from api.lots.manager import LotManager
        from api.orders.manager import OrderManager

        self.user_manager = UserManager(self)
        self.lot_manager = LotManager(self)
        self.order_manager = OrderManager(self)

        self.logger = logging.getLogger("lukovka")

        from api.fuels.accessor import FuelsAccessor

        self.fuels_accessor = FuelsAccessor(self)


store = Store()
