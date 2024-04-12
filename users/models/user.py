import os
from datetime import datetime, date, timezone

from pydantic import BaseModel, EmailStr, Field, model_validator


class User(BaseModel):
    id: str | None
    username: str | None
    email: EmailStr | None
    phone: str | None = Field(pattern="^0\d{9,10}$", default=None)
    password: str
    full_name: str
    birthday: str
    is_admin: bool = False
    is_active: bool
    is_first_login: bool

    class Config:
        from_atributes = True

    @staticmethod
    def model_validate_mongodb(data: dict | None) -> "User":
        if data is None:
            return None

        data["id"] = data.pop("_id").__str__()
        return User.model_validate(data)


class UserRegisterViewModel(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(pattern="^0\d{9,10}$", default=None)
    password: str = Field(min_length=8)
    full_name: str
    birthday: date

    class Config:
        from_atributes = True

    @model_validator(mode="before")
    def validate_identifier(cls, data):
        if not data.get("username") and not data.get("email") and not data.get("phone"):
            raise ValueError("At least one of username, email, phone is required")
        return data

    def to_user(self):
        return User(
            id=None,
            username=self.username,
            email=self.email,
            phone=self.phone,
            password=self.password,
            full_name=self.full_name,
            birthday=self.birthday.strftime(os.getenv("DATE_FORMAT")),
            is_active=True,
            is_first_login=True
        )


class UserLoginViewModel(BaseModel):
    identifier: str
    password: str

    class Config:
        from_atributes = True
