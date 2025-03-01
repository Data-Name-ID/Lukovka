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
        from api.lots.accessor import LotsAccessor
        from api.orders.accessor import OrderAccessor

        self.user_accessor = UserAccessor(self)

        self.order_accessor = OrderAccessor(self)
        self.lot_accessor = LotsAccessor(self)

        from api.auth.manager import UserManager
        from api.lots.manager import LotManager

        self.user_manager = UserManager(self)
        self.lot_manager = LotManager(self)


store = Store()
