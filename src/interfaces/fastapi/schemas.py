from datetime import datetime

from pydantic import BaseModel, NonNegativeFloat

from src.repository.binance_api.models import AnyPaymentWithNotRegistered, CryptoCurrency, FiatCurrency

__all__ = ["ExchangeRateInResponse"]


class ExchangeRateInResponse(BaseModel):
    source_currency: FiatCurrency
    target_currency: FiatCurrency
    exchange_rate: float
    source_amount: NonNegativeFloat
    source_payments: set[AnyPaymentWithNotRegistered]
    target_payments: set[AnyPaymentWithNotRegistered]
    acquisition_time: datetime
    intermediate_crypto: CryptoCurrency
