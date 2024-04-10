from typing import Any
from pymongo.database import Database

from .user_repository import UserRepository


class RepositoryFactory:
    def __init__(self, name: str, db: Database):
        self.name = name
        self.db = db

    def __call__(self) -> Any:
        if self.name == "user":
            return UserRepository(self.db)
        else:
            raise NotImplementedError
