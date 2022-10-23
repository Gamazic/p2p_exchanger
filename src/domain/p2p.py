from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeFloat, root_validator

from src.repository.binance_api.models import (AnyPayment, CryptoCurrency,
                                               FiatCurrency, P2PTradeType)

AnyCurrency = FiatCurrency | CryptoCurrency


class P2PSameCurrencyTypeError(Exception):
    ...


class P2PTradeTypeError(Exception):
    ...


class P2POrder(BaseModel):
    source_currency: AnyCurrency
    target_currency: AnyCurrency
    price: NonNegativeFloat
    amount: NonNegativeFloat
    trade_type: P2PTradeType
    payments: list[AnyPayment]
    datetime: datetime

    @root_validator
    def check_different_currencies_type(cls, values):
        source_currency = values["source_currency"]
        target_currency = values["target_currency"]
        if type(source_currency) == type(target_currency):
            raise P2PSameCurrencyTypeError(
                "source currency and target currency should be different type"
            )
        return values

    @root_validator
    def check_trade_type_corresponds_to_source_currency(cls, values):
        source_currency = values["source_currency"]
        trade_type = values["trade_type"]
        if source_currency in FiatCurrency and trade_type is P2PTradeType.SELL:
            raise P2PTradeTypeError(
                "source currency couldn't be Fiat with SELL trade type"
            )
        elif source_currency in CryptoCurrency and trade_type is P2PTradeType.BUY:
            raise P2PTradeTypeError(
                "source currency couldn't be Crypto with BUY trade type"
            )
        return values


class P2PFilter(BaseModel):
    source_currency: AnyCurrency
    target_currency: AnyCurrency
    min_amount: NonNegativeFloat
    payments: list[AnyPayment] = Field(unique_items=True)

    @root_validator
    def check_different_currencies_type(cls, values):
        source_currency = values["source_currency"]
        target_currency = values["target_currency"]
        if type(source_currency) == type(target_currency):
            raise P2PSameCurrencyTypeError(
                "source currency and target currency should be different type"
            )
        return values

    @root_validator
    def check_payments_match_currency(cls, values):
        source_currency = values["source_currency"]
        target_currency = values["target_currency"]
        payments = values["payments"]
        if source_currency in FiatCurrency:
            for payment in payments:
                payment.validate_currency(source_currency)
        else:
            for payment in payments:
                payment.validate_currency(target_currency)
        return values
