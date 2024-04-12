import time
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from models.user import User


class UserRepository:
    COLLECTION_NAME = "users"

    def __init__(self, db: Database):
        self.collections = db.get_collection(self.COLLECTION_NAME)

    async def find_by_identifier(
        self, identifier: str, session: AgnosticClientSession = None
    ) -> User:
        user_in_db = await self.collections.find_one(
            {
                "$or": [
                    {"username": identifier},
                    {"email": identifier},
                    {"phone": identifier},
                ]
            },
            session=session,
        )

        return User.model_validate_mongodb(user_in_db)

    async def is_exist(self, user: User, session: AgnosticClientSession = None) -> bool:
        for key in ["username", "email", "phone"]:
            if getattr(user, key) is None:
                continue

            user_in_db = await self.find_by_identifier(
                getattr(user, key), session=session
            )
            if user_in_db is not None:
                return True

        return False

    async def create(self, user: User, session: AgnosticClientSession = None) -> str:
        if await self.is_exist(user):
            raise ValueError("User already exists")

        user_in_db = await self.collections.insert_one(
            user.model_dump(), session=session
        )
        return user_in_db.inserted_id

    async def update_first_login(
        self, user: User, session: AgnosticClientSession = None
    ) -> str:
        user_in_db = await self.collections.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": {"is_first_login": False}},
            session=session,
        )
        return user_in_db.upserted_id
