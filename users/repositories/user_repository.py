from pymongo.database import Database, Collection
from bson import ObjectId

from models.user import User


class UserRepository:
    collections: Collection

    def __init__(self, db: Database):
        self.collections = db.get_collection("users")

    def find_by_identifier(self, identifier: str) -> User:
        user_in_db = self.collections.find_one(
            {"$or": [{"username": identifier}, {"email": identifier}, {"phone": identifier}]}
        )

        if user_in_db is None:
            return None

        user_in_db["id"] = user_in_db.pop("_id").__str__()
        user = User.model_validate(user_in_db)
        return user

    def is_exist(self, user: User) -> bool:
        for key in ["username", "email", "phone"]:
            if getattr(user, key) is None:
                continue

            user_in_db = self.find_by_identifier(getattr(user, key))
            if user_in_db is not None:
                return True

        return False

    def create(self, user: User) -> str:
        if self.is_exist(user):
            raise ValueError("User already exists")
        print(user.model_dump())

        return self.collections.insert_one(user.model_dump()).inserted_id

    def update(self, user: User) -> str:
        return self.collections.update_one(
            {"_id": ObjectId(user.id)}, {"$set": user.model_dump()}
        ).upserted_id
