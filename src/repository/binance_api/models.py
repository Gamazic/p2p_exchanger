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
    QIWI = auto()
    YandexMoneyNew = auto()
    MTSBank = auto()
    HomeCreditBank = auto()
    PostBankNew = auto()
    RUBfiatbalance = auto()
    Payeer = auto()
    UralsibBank = auto()
    AkBarsBank = auto()
    Mobiletopup = auto()
    BCSBank = auto()
    Advcash = auto()
    RenaissanceCredit = auto()
    RussianStandardBank = auto()
    BankSaintPetersburg = auto()
    UniCreditRussia = auto()
    ABank = auto()
    OTPBankRussia = auto()
    CreditEuropeBank = auto()
    CitibankRussia = auto()
    CashInPerson = auto()
    RaiffeisenBankAval = auto()

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


class TradeMethod(CamelModel):
    identifier: Payments


class AdvSearchApi(CamelModel):
    max_single_trans_amount: NonNegativeFloat
    min_single_trans_amount: NonNegativeFloat
    price: NonNegativeFloat
    trade_methods: list[TradeMethod]


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
