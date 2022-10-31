from fastapi import APIRouter, Depends, Query
from pydantic import NonNegativeFloat

from src.domain.fiat import FiatAnyCryptoFilter, FiatParams
from src.interfaces.fastapi.container import fiat_any_crypto_exchanger
from src.interfaces.fastapi.schemas import ExchangeRateInResponse
from src.repository.binance_api.models import (AnyPayment, CryptoCurrency,
                                               FiatCurrency)
from src.services.exchangers import FiatAnyCryptoExchangerService

api = APIRouter()


@api.get("/exchange_rate", response_model=ExchangeRateInResponse)
async def get_best_exchange_rate(
    source_currency: FiatCurrency,
    target_currency: FiatCurrency,
    intermediate_cryptos: list[CryptoCurrency] = Query([]),
    min_amount: NonNegativeFloat = Query(0),
    source_payments: list[AnyPayment] = Query([]),
    target_payments: list[AnyPayment] = Query([]),
    exchanger_service: FiatAnyCryptoExchangerService = Depends(
        fiat_any_crypto_exchanger
    ),
):
    filter = FiatAnyCryptoFilter(
        source_params=FiatParams(
            currency=source_currency,
            min_amount=min_amount,
            payments=frozenset(source_payments),
        ),
        target_params=FiatParams(
            currency=target_currency, min_amount=0, payments=frozenset(target_payments)
        ),
        intermediate_cryptos=intermediate_cryptos,
    )
    fiat_order = await exchanger_service.find_best_price(filter)
    response = ExchangeRateInResponse(
        source_currency=fiat_order.source_order.source_currency,
        target_currency=fiat_order.target_order.target_currency,
        exchange_rate=fiat_order.price,
        acquisition_time=fiat_order.source_order.datetime,
        intermediate_crypto=fiat_order.source_order.target_currency,
        source_amount=fiat_order.source_order.amount,
        source_payments=fiat_order.source_order.payments,
        target_payments=fiat_order.target_order.payments,
    )
    return response
