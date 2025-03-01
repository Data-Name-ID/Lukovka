from core.store import Store


class OrderManager:
    def __init__(self, store: Store) -> None:
        self.store = store
