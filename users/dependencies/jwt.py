import os
import jwt
from datetime import datetime, timezone


class JWTAuthentication:
    def generate_token(self, payload: dict) -> str:
        raise NotImplementedError

    def get_payload(self, token: str) -> dict:
        raise NotImplementedError

    def is_valid(self, token: str, user_id: int) -> bool:
        payload = self.get_payload(token)

        if "expired_at" not in payload or "user_id" not in payload:
            return False

        return payload["user_id"] == user_id and datetime.now(timezone.utc).strftime(os.getenv("DATETIME_FORMAT")) < payload["expired_at"]


class JWTAuthenticationFactory:
    @staticmethod
    def create(algorithm: str, private_key: str = None, public_key: str = None) -> JWTAuthentication:
        if algorithm == "HS256":
            return JWTAuthenticationSHA256(private_key)
        elif algorithm == "RS256":
            return JWTAuthenticationRSA(private_key, public_key)
        else:
            raise ValueError("Algorithm is not supported")


class JWTAuthenticationSHA256(JWTAuthentication):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_token(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def get_payload(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=["HS256"])


class JWTAuthenticationRSA(JWTAuthentication):
    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    def generate_token(self, payload: dict) -> str:
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def get_payload(self, token: str) -> dict:
        return jwt.decode(token, self.public_key, algorithms=["RS256"])
