import os
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from models.campaign import Campaign, CampaignCreateViewModel
from repositories import CampaignRepository
from dependencies.database import MongoDb
from dependencies.jwt import JWTAuthenticationFactory, JWTAuthentication


router = APIRouter()


@router.post("/campaigns/create")
async def create_campaign(
    campaign_view: CampaignCreateViewModel,
    authorization: Annotated[str, Header()] = None,
) -> JSONResponse:
    campaign_repository = CampaignRepository(MongoDb.database)
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if not jwt_authentication.is_admin(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    await campaign_repository.create(campaign_view.to_campaign())

    return JSONResponse(status_code=201, content="Campaign created")
