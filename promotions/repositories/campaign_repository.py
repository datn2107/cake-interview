import datetime
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession
from bson import ObjectId

from models.campaign import Campaign


class CampaignRepository:
    COLLECTION_NAME = "campaign"

    def __init__(self, db: Database):
        self.collections = db.get_collection(self.COLLECTION_NAME)

    async def find_available_campaign(
        self, session: AgnosticClientSession = None
    ) -> Campaign:
        campaign = await self.collections.find_one(
            {
                "is_available": True,
                "remaining_vouchers": {"$gt": 0},
            },
            session=session,
        )

        return Campaign.model_validate_mongodb(campaign)

    async def create(
        self, campaign: Campaign, session: AgnosticClientSession = None
    ) -> str:
        campaign_in_db = await self.collections.insert_one(
            campaign.model_dump(), session=session
        )

        return campaign_in_db.inserted_id

    async def decrease_voucher_from_campaign(
        self, campaign_id: str, session: AgnosticClientSession = None
    ):
        campaign = await self.collections.find_one({"_id": ObjectId(campaign_id)}, session=session)

        if campaign is None:
            return None

        if campaign["remaining_vouchers"] == 0:
            return None

        campaign = await self.collections.update_one(
            {"_id": ObjectId(campaign_id)},
            {"$inc": {"remaining_vouchers": -1}},
            session=session,
        )

        return campaign.upserted_id
