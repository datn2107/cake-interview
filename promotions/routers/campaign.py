import os
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from models.campaign import CampaignCreateViewModel
from repositories import CampaignRepository
from dependencies.database import MongoDb
from .handler.authentication import verfiy_token


router = APIRouter()


@router.post("/campaigns/create")
async def create_campaign(
    campaign_view: CampaignCreateViewModel,
    authorization: Annotated[str, Header()] = None,
) -> JSONResponse:
    campaign_repository = CampaignRepository(MongoDb.database)

    verfiy_token(authorization, is_admin=True)

    await campaign_repository.create(campaign_view.to_campaign())

    return JSONResponse(status_code=201, content="Campaign created")
