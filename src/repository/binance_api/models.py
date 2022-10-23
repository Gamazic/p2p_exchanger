from enum import auto
from typing import Literal

from fastapi_utils.enums import StrEnum
from humps import camel  # type: ignore
from pydantic import (BaseModel, Field, NonNegativeFloat, NonNegativeInt,
                      PositiveInt)


class Country(StrEnum):
    Russia = auto()


class FiatCurrency(StrEnum):
    KZT = auto()
    RUB = auto()


class CryptoCurrency(StrEnum):
    USDT = auto()
    BTC = auto()
    BUSD = auto()
    BNB = auto()
    ETH = auto()
    SHIB = auto()


class PaymentDoesntMatchCurrencyError(Exception):
    ...


class PaymentBase(StrEnum):
    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        raise NotImplementedError()


class RuPayment(PaymentBase):
    TinkoffNew = auto()
    RosBankNew = auto()
    RaiffeisenBank = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.RUB:
            raise PaymentDoesntMatchCurrencyError


class KztPayment(PaymentBase):
    KaspiBank = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.KZT:
            raise PaymentDoesntMatchCurrencyError


Payments = RuPayment | KztPayment

class P2PTradeType(StrEnum):
    BUY = auto()
    SELL = auto()


class CamelModel(BaseModel):
    class Config:
        alias_generator = camel.case
        allow_population_by_field_name = True


class SearchApiParams(CamelModel):
    asset: CryptoCurrency
    fiat: FiatCurrency
    trade_type: P2PTradeType
    rows: PositiveInt = 10
    page: PositiveInt = 1
    publisher_type: Literal["merchant"] | None = None
    pay_types: list[Payments] = Field(default_factory=list)
    countries: list[Country] = Field(default_factory=list)
    trans_amount: NonNegativeFloat | None = None
    pro_merchant_ads: bool | None = None


class AdvSearchApi(CamelModel):
    maxSingleTransAmount: NonNegativeFloat
    minSingleTransAmount: NonNegativeFloat
    price: NonNegativeFloat


class AdvertiserSearchApi(CamelModel):
    nick_name: str
    month_finish_rate: float = Field(ge=0, le=1)
    month_order_count: NonNegativeInt
    user_grade: NonNegativeInt
    user_type: Literal["user", "merchant"]
    user_identity: Literal["MASS_MERCHANT", ""]


class P2POrderSearchApi(CamelModel):
    adv: AdvSearchApi
    advertiser: AdvertiserSearchApi


class SearchApiResponse(CamelModel):
    code: str
    data: list[P2POrderSearchApi]
    success: bool
    total: NonNegativeInt
