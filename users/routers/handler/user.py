import os
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as AgnosticClientSession

from models.user import User, UserLoginViewModel
from repositories import UserRepository
from dependencies.database import MongoDb
from message_queue.producer.promotion import push_promotion_message


@MongoDb.transaction
async def create_user_transaction(
    user: User, user_repository: UserRepository, session: AgnosticClientSession = None
):
    if await user_repository.is_exist(user, session=session):
        raise HTTPException(status_code=400, detail="User already exists")

    await user_repository.create(user, session=session)


@MongoDb.transaction
async def verify_and_login_transaction(
    user_login: UserLoginViewModel,
    user_repository: UserRepository,
    session: AgnosticClientSession = None,
):
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
