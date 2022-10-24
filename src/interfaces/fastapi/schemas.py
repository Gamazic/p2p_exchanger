from datetime import datetime

from pydantic import BaseModel

from src.repository.binance_api.models import CryptoCurrency, FiatCurrency


class ExchangeRateInResponse(BaseModel):
    source_currency: FiatCurrency
    target_currency: FiatCurrency
    exchange_rate: float
    acquisition_time: datetime
    intermediate_crypto: CryptoCurrency
