from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from bson import ObjectId

from models.user import User


class UserRepository:
    collections: Collection

    def __init__(self, db: Database):
        self.collections = db.get_collection("users")

    async def find_by_identifier(self, identifier: str) -> User:
        user_in_db = await self.collections.find_one(
            {"$or": [{"username": identifier}, {"email": identifier}, {"phone": identifier}]}
        )

        if user_in_db is None:
            return None

        user_in_db["id"] = user_in_db.pop("_id").__str__()
        user = User.model_validate(user_in_db)
        return user

    async def is_exist(self, user: User) -> bool:
        for key in ["username", "email", "phone"]:
            if getattr(user, key) is None:
                continue

            user_in_db = await self.find_by_identifier(getattr(user, key))
            if user_in_db is not None:
                print(user_in_db.model_dump())
                return True

        return False

    async def create(self, user: User) -> str:
        if await self.is_exist(user):
            raise ValueError("User already exists")

        user_in_db = await self.collections.insert_one(user.model_dump())
        return user_in_db.inserted_id

    async def update(self, user: User) -> str:
        user_in_db = await self.collections.update_one(
            {"_id": ObjectId(user.id)}, {"$set": user.model_dump()}
        )
        return user_in_db.upserted_id