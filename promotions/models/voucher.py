import os
from datetime import datetime

from pydantic import BaseModel


class Voucher(BaseModel):
    id: str | None
    user_id: str
    campaign_id: str
    description: str | None
    expired_at: datetime
    discount: int

    class Config:
        from_atributes = True
