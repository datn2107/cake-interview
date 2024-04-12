from datetime import datetime, timezone
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from bson import ObjectId

from models.voucher import Voucher


class VoucherRepository:
    COLLECTION_NAME = "voucher"

    collections: Collection

    def __init__(self, db: Database):
        self.collections = db.get_collection(self.COLLECTION_NAME)

    async def find_by_id(self, voucher_id: str) -> Voucher:
        voucher = await self.collections.find_one({"_id": ObjectId(voucher_id)})

        return Voucher.model_validate_mongodb(voucher)

    async def find_available_vouchers(self, user_id: str) -> List[Voucher]:
        vouchers = [
            voucher
            async for voucher in self.collections.find(
                {"user_id": user_id, "expired_at": {"$gte": datetime.now(timezone.utc)}}
            )
        ]

        return [Voucher.model_validate_mongodb(voucher) for voucher in vouchers]

    async def create(self, voucher: Voucher) -> str:
        voucher_in_db = await self.collections.insert_one(voucher.model_dump())
        return voucher_in_db.inserted_id

    async def redeem(self, voucher: Voucher) -> str:
        voucher_in_db = await self.collections.update_one(
            {"_id": ObjectId(voucher.id)}, {"$set": {"redeemed_at": datetime.now()}}
        )
        return voucher_in_db.upserted_id
