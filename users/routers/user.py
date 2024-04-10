import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependencies.database import database
from dependencies.jwt import JWTAuthenticationFactory, JWTAuthentication
from repositories import RepositoryFactory, UserRepository
from models.user import User, UserRegisterViewModel, UserLoginViewModel

router = APIRouter()
user_repository = RepositoryFactory("user", database)
jwt_authentication = JWTAuthenticationFactory(
    "RSA", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
)


@router.post("/users/register")
async def create_user(
    user_register: UserRegisterViewModel,
    user_repository: UserRepository = Depends(user_repository),
) -> JSONResponse:
    user = user_register.to_user()
    if user_repository.is_exist(user):
        return JSONResponse(status_code=400, content="User already exists")

    user_repository.create(user)

    return JSONResponse(status_code=201, content="User created")


@router.post("/users/login")
async def login_user(
    user_login: UserLoginViewModel,
    user_repository: UserRepository = Depends(user_repository),
    jwt_authentication: JWTAuthentication = Depends(jwt_authentication),
) -> JSONResponse:
    user = user_repository.find_by_identifier(user_login.identifier)
    if user is None:
        return JSONResponse(status_code=404, content="User not found")

    if user.password != user_login.password:
        return JSONResponse(status_code=401, content="Password is incorrect")

    if user.is_first_login:
        user.is_first_login = False
        user_repository.update(user)

        # TO DO: send user infor to promotion service

    expired_at = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("JWT_EXPIRED_MINUTES"))
    )
    payload = {
        "user_id": user.id,
        "user_identifier": user_login.identifier,
        "expired_at": expired_at.strftime(os.getenv("DATETIME_FORMAT")),
    }
    token = jwt_authentication.generate_token(payload)

    return JSONResponse(status_code=200, content={"token": token})
