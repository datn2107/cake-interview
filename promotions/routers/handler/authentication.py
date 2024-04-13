import os
from fastapi import HTTPException

from dependencies.jwt import JWTAuthenticationFactory


def verfiy_token(
    bearer_token: str | None, user_id: str | None = None, is_admin: bool = False
):
    jwt_authentication = JWTAuthenticationFactory.create(
        "RS256", os.getenv("PRIVATE_KEY"), os.getenv("PUBLIC_KEY")
    )

    if bearer_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = bearer_token.split(" ")[1]
    if not is_admin and not jwt_authentication.is_valid(token, user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if is_admin and not jwt_authentication.is_admin(bearer_token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return True
