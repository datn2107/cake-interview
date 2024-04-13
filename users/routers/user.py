import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from dependencies.database import MongoDb
from dependencies.jwt import JWTAuthenticationFactory
from message_queue.producer.promotion import push_promotion_message
from repositories import UserRepository
from models.user import UserRegisterViewModel, UserLoginViewModel
from .handler.user import create_user_transaction, verify_and_login_transaction

router = APIRouter()


@router.post("/users/register")
async def create_user(user_register: UserRegisterViewModel) -> JSONResponse:
    user_repository = UserRepository(MongoDb.database)

    user = user_register.to_user()
    await create_user_transaction(user, user_repository)

    return JSONResponse(status_code=201, content="User created")


@router.post("/users/login")
async def login_user(user_login: UserLoginViewModel) -> JSONResponse:
    user_repository = UserRepository(MongoDb.database)
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    user = await verify_and_login_transaction(user_login, user_repository)

    expired_at = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("JWT_EXPIRED_MINUTES"))
    )
    payload = {
        "user_id": user.id,
        "user_identifier": user_login.identifier,
        "expired_at": expired_at.strftime(os.getenv("DATETIME_FORMAT")),
        "is_admin": user.is_admin,
    }
    token = jwt_authentication.generate_token(payload)

    return JSONResponse(status_code=200, content={"user_id": user.id, "token": token})
