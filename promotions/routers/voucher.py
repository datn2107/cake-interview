import os
import json
from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from models.voucher import Voucher
from repositories import VoucherRepository
from dependencies.jwt import JWTAuthenticationFactory
from dependencies.database import MongoDb
from .handler.authentication import verfiy_token
from .handler.voucher import redeem_voucher_transaction


router = APIRouter()


@router.post("/vouchers")
async def get_vouchers(
    user_id: str,
    authorization: Annotated[str | None, Header()] = None,
    request: Request = None,
) -> JSONResponse:
    voucher_repository = VoucherRepository(MongoDb.database)

    verfiy_token(authorization, user_id)

    vouchers = await voucher_repository.find_available_vouchers(user_id)
    vouchers = json.dumps([voucher.model_dump() for voucher in vouchers], default=str)

    return JSONResponse(status_code=200, content=vouchers)


@router.post("/vouchers/redeem")
async def redeem_voucher(
    voucher_id: str, user_id: str, authorization: Annotated[str, Header()] = None
) -> JSONResponse:
    voucher_repository = VoucherRepository(MongoDb.database)

    verfiy_token(authorization, user_id)

    await redeem_voucher_transaction(user_id, voucher_id, voucher_repository)

    return JSONResponse(status_code=200, content="Voucher redeemed")
