import os
from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse

from models.voucher import Voucher
from repositories import VoucherRepository
from dependencies.jwt import JWTAuthenticationFactory
from dependencies.database import MongoDb


router = APIRouter()


@router.post("/vouchers")
async def get_vouchers(
    user_id: str, authorization: Annotated[str | None, Header()] = None, request: Request = None
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

    return JSONResponse(status_code=200, content=vouchers)


@router.post("/vouchers/redeem")
async def redeem_voucher(
    voucher_id: str, user_id: str, authorization: Annotated[str, Header()] = None
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

    voucher = await voucher_repository.find_by_id(voucher_id)

    if voucher is None:
        raise HTTPException(status_code=404, detail="Voucher not found")

    if voucher.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if voucher.expired_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Voucher expired")

    await voucher_repository.redeem(voucher_id)

    return JSONResponse(status_code=200, content="Voucher redeemed")
