class Store:
    def __init__(self) -> None:
        from core.config import Config

        self.config = Config()

        from core.email import EmailManager
        from core.jwt import JWTManager

        self.email = EmailManager(self)
        self.jwt = JWTManager(self)

        from api.auth.accessor import UserAccessor
        from core.db import DatabaseAccessor
        from api.orders.accessor import OrderAccessor

        self.db = DatabaseAccessor(self)
        self.user_accessor = UserAccessor(self)
        self.order_accessor = OrderAccessor(self)

        from api.auth.manager import UserManager

        self.user_manager = UserManager(self)


store = Store()
