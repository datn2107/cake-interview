import os
import jwt
from datetime import datetime, timezone


class JWTAuthentication:
    def generate_token(self, payload: dict) -> str:
        raise NotImplementedError


class JWTAuthenticationFactory:
    @staticmethod
    def create(
        algorithm: str, private_key: str = None, public_key: str = None
    ) -> JWTAuthentication:
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


class JWTAuthenticationRSA(JWTAuthentication):
    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    def generate_token(self, payload: dict) -> str:
        return jwt.encode(payload, self.private_key, algorithm="RS256")
