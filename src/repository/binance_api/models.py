from enum import auto
from typing import Literal

from fastapi_utils.enums import StrEnum
from humps import camel  # type: ignore
from pydantic import (BaseModel, Field, NonNegativeFloat, NonNegativeInt,
                      PositiveInt, validator)


class Country(StrEnum):
    Russia = auto()


class FiatCurrency(StrEnum):
    KZT = auto()
    RUB = auto()


class CryptoCurrency(StrEnum):
    BTC = auto()
    ETH = auto()
    BNB = auto()
    USDT = auto()
    BUSD = auto()
    SHIB = auto()


class PaymentDoesntMatchCurrencyError(Exception):
    ...


class PaymentBase(StrEnum):
    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        raise NotImplementedError()


class RuPayment(PaymentBase):
    QIWI = auto()
    ABank = auto()
    Payeer = auto()
    MTSBank = auto()
    BCSBank = auto()
    Advcash = auto()
    AkBarsBank = auto()
    TinkoffNew = auto()
    RosBankNew = auto()
    UralsibBank = auto()
    PostBankNew = auto()
    Mobiletopup = auto()
    CashInPerson = auto()
    OTPBankRussia = auto()
    CitibankRussia = auto()
    RaiffeisenBank = auto()
    YandexMoneyNew = auto()
    HomeCreditBank = auto()
    RUBfiatbalance = auto()
    UniCreditRussia = auto()
    CreditEuropeBank = auto()
    RenaissanceCredit = auto()
    RaiffeisenBankAval = auto()
    RussianStandardBank = auto()
    BankSaintPetersburg = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.RUB:
            raise PaymentDoesntMatchCurrencyError


class KztPayment(PaymentBase):
    QIWI = auto()
    BANK = auto()
    KaspiBank = auto()
    HalykBank = auto()
    ForteBank = auto()
    JysanBank = auto()
    Mobiletopup = auto()
    CenterCreditBank = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.KZT:
            raise PaymentDoesntMatchCurrencyError


class NonRegisteredPayment(PaymentBase):
    UnknownPayment = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        return


AnyPayment = RuPayment | KztPayment
AnyPaymentWithNotRegistered = RuPayment | KztPayment | NonRegisteredPayment


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
    pay_types: frozenset[AnyPayment] = Field(default_factory=set)
    countries: frozenset[Country] = Field(default_factory=set)
    trans_amount: NonNegativeFloat | None = None
    pro_merchant_ads: bool | None = None

    class Config:
        frozen = True


class TradeMethod(CamelModel):
    identifier: AnyPayment | str

    @validator("identifier")
    def drop_not_registered_payments(cls, v):
        if not isinstance(v, PaymentBase):
            return NonRegisteredPayment.UnknownPayment
        return v


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
