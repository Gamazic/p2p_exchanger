from datetime import datetime

from pydantic import BaseModel, NonNegativeFloat

from src.repository.binance_api.models import (AnyPaymentWithNotRegistered,
                                               CryptoCurrency, FiatCurrency)


class ExchangeRateInResponse(BaseModel):
    source_currency: FiatCurrency
    target_currency: FiatCurrency
    exchange_rate: float
    source_amount: NonNegativeFloat
    source_payments: list[AnyPaymentWithNotRegistered]
    target_payments: list[AnyPaymentWithNotRegistered]
    acquisition_time: datetime
    intermediate_crypto: CryptoCurrency
