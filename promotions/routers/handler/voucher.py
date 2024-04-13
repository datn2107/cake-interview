import os
from datetime import datetime, timezone
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from repositories import VoucherRepository
from dependencies.database import MongoDb


@MongoDb.transaction
async def redeem_voucher_transaction(
    user_id: str,
    voucher_id: str,
    voucher_repository: VoucherRepository,
    session: AgnosticClientSession = None,
):
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
