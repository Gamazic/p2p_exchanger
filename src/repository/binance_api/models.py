from enum import auto, Enum
from typing import Literal

from humps import camel  # type: ignore
from pydantic import (BaseModel, Field, NonNegativeFloat, NonNegativeInt,
                      PositiveInt, validator)


class StrEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Country(StrEnum):
    Russia = auto()


class FiatCurrency(StrEnum):
    RUB = auto()
    KZT = auto()  # Kazakh
    TRY = auto()  # Turkish
    GEL = auto()  # Georgian
    EUR = auto()
    USD = auto()
    AED = auto()  # Emirates
    # JPY = auto()  # Japanese
    CNY = auto()  # Chinese


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


class RubPayment(PaymentBase):
    QIWI = auto()
    ABank = auto()
    Payeer = auto()
    # MTSBank = auto()
    # BCSBank = auto()
    # Advcash = auto()
    # AkBarsBank = auto()
    TinkoffNew = auto()
    # RosBankNew = auto()
    # UralsibBank = auto()
    PostBankNew = auto()
    # Mobiletopup = auto()
    # CashInPerson = auto()
    # OTPBankRussia = auto()
    # CitibankRussia = auto()
    RaiffeisenBank = auto()
    # YandexMoneyNew = auto()
    # HomeCreditBank = auto()
    # RUBfiatbalance = auto()
    # UniCreditRussia = auto()
    # CreditEuropeBank = auto()
    # RenaissanceCredit = auto()
    # RaiffeisenBankAval = auto()
    # RussianStandardBank = auto()
    # BankSaintPetersburg = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.RUB:
            raise PaymentDoesntMatchCurrencyError(f"Payment {FiatCurrency.RUB} doesn't match"
                                                  f"{currency} currency")


class KztPayment(PaymentBase):
    # QIWI = auto()
    # BANK = auto()
    KaspiBank = auto()
    HalykBank = auto()
    ForteBank = auto()
    JysanBank = auto()
    # Mobiletopup = auto()
    # CenterCreditBank = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.KZT:
            raise PaymentDoesntMatchCurrencyError(f"Payment {FiatCurrency.KZT} doesn't match"
                                                  f"{currency} currency")


class TryPayment(PaymentBase):
    Ziraat = auto()
    # BANK = auto()
    QNB = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.TRY:
            raise PaymentDoesntMatchCurrencyError(f"Payment {FiatCurrency.TRY} doesn't match"
                                                  f"{currency} currency")


class GelPayment(PaymentBase):
    BankofGeorgia = auto()
    LIBERTYBANK = auto()
    # TBCbank = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.GEL:
            raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
                                                  f" {FiatCurrency.GEL} payments")


class EurPayment(PaymentBase):
    Zen = auto()
    Wise = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.EUR:
            raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
                                                  f" {FiatCurrency.EUR} payments")

class UsdPayment(PaymentBase):
    AirTM = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.USD:
            raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
                                                  f" {FiatCurrency.USD} payments")

class AedPayment(PaymentBase):
    ADCB = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.AED:
            raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
                                                  f" {FiatCurrency.AED} payments")

# class JpyPayment(PaymentBase):
#     Bank = auto()
#
#     @classmethod
#     def validate_currency(cls, currency: FiatCurrency):
#         if currency is not FiatCurrency.JPY:
#             raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
#                                                   f" {FiatCurrency.JPY} payments")


class CnyPayment(PaymentBase):
    Alipay = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        if currency is not FiatCurrency.CNY:
            raise PaymentDoesntMatchCurrencyError(f"Currency {currency} doesn't match"
                                                  f" {FiatCurrency.CNY} payments")


class NonRegisteredPayment(PaymentBase):
    UnknownPayment = auto()

    @classmethod
    def validate_currency(cls, currency: FiatCurrency):
        return


AnyPayment = RubPayment | KztPayment | TryPayment | GelPayment | EurPayment | UsdPayment | AedPayment | CnyPayment
AnyPaymentWithNotRegistered = AnyPayment | NonRegisteredPayment


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
    user_grade: NonNegativeInt | None  # Only once it was None
    user_type: Literal["user", "merchant"] | None  # Only once it was None
    user_identity: Literal["MASS_MERCHANT", "BLOCK_MERCHANT", ""] | None  # Only once it was None


class P2POrderSearchApi(CamelModel):
    adv: AdvSearchApi
    advertiser: AdvertiserSearchApi


class SearchApiResponse(CamelModel):
    code: str
    data: list[P2POrderSearchApi]
    success: bool
    total: NonNegativeInt
