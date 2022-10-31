from pydantic import BaseModel, NonNegativeFloat, root_validator, validator

from src.domain.p2p import P2POrder
from src.repository.binance_api.models import (AnyPayment, CryptoCurrency,
                                               FiatCurrency, P2PTradeType)


class SameFiatCurrencyError(Exception):
    ...


class FiatParams(BaseModel):
    currency: FiatCurrency
    min_amount: NonNegativeFloat
    payments: frozenset[AnyPayment]

    @root_validator
    def check_payments_match_currency(cls, values):
        for payment in values["payments"]:
            payment.validate_currency(values["currency"])
        return values


class FiatBundle(BaseModel):
    source_params: FiatParams
    target_params: FiatParams

    @root_validator
    def check_different_currencies(cls, values):
        source_currency = values["source_params"].currency
        target_currency = values["target_params"].currency
        if source_currency is target_currency:
            raise SameFiatCurrencyError(
                f"Expected different source and target currencies."
                f"Got {source_currency=}, {target_currency=}"
            )
        return values

    # TODO Does it need any validation of source and target min amount?
    # @root_validator
    # def check_source_target_min_amount(cls, values):
    #     return values


class FiatFixedCryptoFilter(FiatBundle):
    intermediate_crypto: CryptoCurrency


class FiatAnyCryptoFilter(FiatBundle):
    intermediate_cryptos: list[CryptoCurrency]


class DifferentP2PCryptoError(Exception):
    ...


class BadP2POrderTypeError(Exception):
    ...


class FiatOrder(BaseModel):
    source_order: P2POrder
    target_order: P2POrder
    price: NonNegativeFloat

    @validator("source_order")
    def check_source_order_is_buy(cls, v):
        if v.trade_type is not P2PTradeType.BUY:
            raise BadP2POrderTypeError(
                f"Expected source trade type is BUY, got {v.trade_type}"
            )
        return v

    @validator("target_order")
    def check_target_order_is_sell(cls, v):
        if v.trade_type is not P2PTradeType.SELL:
            raise BadP2POrderTypeError(
                f"Expected source trade type is SELL, got {v.trade_type}"
            )
        return v

    @root_validator
    def check_different_fiat_in_orders(cls, values):
        source_fiat_currency = values["source_order"].source_currency
        target_fiat_currency = values["target_order"].target_currency
        if source_fiat_currency is target_fiat_currency:
            raise SameFiatCurrencyError(
                f"Expected different source and target currencies."
                f"Got {source_fiat_currency=}, {target_fiat_currency=}"
            )
        return values

    @root_validator
    def check_same_crypto_in_orders(cls, values):
        source_crypto = values["source_order"].target_currency
        target_crypto = values["target_order"].source_currency
        if source_crypto is not target_crypto:
            raise DifferentP2PCryptoError(
                f"Expected same crypto currency,"
                f"got f{source_crypto=}, {target_crypto=}"
            )
        return values
