import datetime
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from bson import ObjectId

from models.campaign import Campaign


class CampaignRepository:
    COLLECTION_NAME = "campaign"

    collections: Collection

    def __init__(self, db: Database):
        self.collections = db.get_collection(self.COLLECTION_NAME)

    async def find_available_campaign(self, user_id: str) -> Campaign:
        campaign = await self.collections.find_one(
            {"user_id": user_id, "remaining_vouchers": {"$gt": 0}}
        )

        if campaign is None:
            return None

        campaign["id"] = campaign.pop("_id").__str__()
        return Campaign.model_validate(campaign) 

    async def create(self, campaign: Campaign) -> str:
        campaign_in_db = await self.collections.insert_one(campaign.model_dump())
        return campaign_in_db.inserted_id

    async def get_voucher_from_campaign(self, campaign_id: str) -> str:
        campaign = await self.collections.find_one({"_id": ObjectId(campaign_id)})

        if campaign is None:
            return None

        if campaign["remaining_vouchers"] == 0:
            return None

        await self.collections.update_one(
            {"_id": ObjectId(campaign_id)},
            {"$inc": {"remaining_vouchers": -1}},
        )

        return campaign["voucher_id"]
