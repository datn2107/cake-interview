import os
from datetime import datetime

from pydantic import BaseModel


class Campaign(BaseModel):
    id: str | None
    name: str
    discount: int
    voucher_duration: int
    remaining_vouchers: int
    number_of_vouchers: int
    is_available: bool
    description: str | None

    class Config:
        from_atributes = True
