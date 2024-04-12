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


router = APIRouter()


@router.post("/vouchers")
async def get_vouchers(
    user_id: str,
    authorization: Annotated[str | None, Header()] = None,
    request: Request = None,
) -> JSONResponse:
    voucher_repository = VoucherRepository(MongoDb.database)
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if not jwt_authentication.is_valid(token, user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")

    vouchers = await voucher_repository.find_available_vouchers(user_id)
    vouchers = json.dumps([voucher.model_dump() for voucher in vouchers], default=str)

    return JSONResponse(status_code=200, content=vouchers)


@router.post("/vouchers/redeem")
async def redeem_voucher(
    voucher_id: str, user_id: str, authorization: Annotated[str, Header()] = None
) -> JSONResponse:
    @MongoDb.transaction
    async def redeem_voucher_transaction(session: AgnosticClientSession):
        voucher = await voucher_repository.find_by_id(voucher_id, session=session)

        if voucher is None:
            raise HTTPException(status_code=404, detail="Voucher not found")

        if voucher.user_id != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if voucher.expired_at < datetime.now(timezone.utc).strftime(
            os.getenv("DATETIME_FORMAT")
        ):
            raise HTTPException(status_code=400, detail="Voucher expired")

        await voucher_repository.redeem(voucher, session=session)

    voucher_repository = VoucherRepository(MongoDb.database)
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if not jwt_authentication.is_valid(token, user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")

    await redeem_voucher_transaction()

    return JSONResponse(status_code=200, content="Voucher redeemed")
