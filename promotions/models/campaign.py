import os
from datetime import datetime
from pydantic import BaseModel

from .base import MongoDbBaseModel


class Campaign(MongoDbBaseModel):
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


class CampaignCreateViewModel(BaseModel):
    name: str
    discount: int
    voucher_duration: int
    number_of_vouchers: int
    description: str | None

    def to_campaign(self):
        return Campaign(
            id=None,
            name=self.name,
            discount=self.discount,
            voucher_duration=self.voucher_duration,
            remaining_vouchers=self.number_of_vouchers,
            number_of_vouchers=self.number_of_vouchers,
            is_available=True,
            description=self.description,
        )
