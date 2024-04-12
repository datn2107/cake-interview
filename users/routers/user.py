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


router = APIRouter()


@router.post("/users/register")
async def create_user(user_register: UserRegisterViewModel) -> JSONResponse:
    @MongoDb.transaction
    async def create_user(session: AgnosticClientSession):
        if await user_repository.is_exist(user, session=session):
            raise HTTPException(status_code=400, detail="User already exists")

        await user_repository.create(user, session=session)

    user_repository = UserRepository(MongoDb.database)

    user = user_register.to_user()
    await create_user()

    return JSONResponse(status_code=201, content="User created")


@router.post("/users/login")
async def login_user(user_login: UserLoginViewModel) -> JSONResponse:
    @MongoDb.transaction
    async def verify_and_login(session: AgnosticClientSession):
        user = await user_repository.find_by_identifier(
            user_login.identifier, session=session
        )

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.password != user_login.password:
            raise HTTPException(status_code=401, detail="Invalid password")

        if user.is_first_login:
            user.is_first_login = False
            await user_repository.update_first_login(user, session=session)

            payload = {"user_id": user.id, "user_identifier": user_login.identifier}
            await push_promotion_message(payload, os.getenv("MQ_PROMOTION_ROUTING_KEY"))

        return user

    user_repository = UserRepository(MongoDb.database)
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    user = await verify_and_login()

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
