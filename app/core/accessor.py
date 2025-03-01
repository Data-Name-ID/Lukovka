from sqlmodel import SQLModel

from core.store import Store


class CoreAccessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    @staticmethod
    def make_condition(value: str, column: SQLModel) -> bool | None:
        return column == value if value else None
