from pydantic import NonNegativeFloat
from starlite import Controller, Dependency, Parameter, get

from src.domain.fiat import FiatAnyCryptoFilter, FiatParams
from src.interfaces.starlite.models import ExchangeRateInResponse
from src.repository.binance_api.models import (AnyPayment, CryptoCurrency,
                                               FiatCurrency)
from src.services.exchangers import FiatAnyCryptoExchangerService


class ExchangeRateController(Controller):
    path = "/best_exchange_rate"

    @get()
    async def get_best_exchange_rate(
        self,
        source_currency: FiatCurrency,
        target_currency: FiatCurrency,
        intermediate_cryptos: list[CryptoCurrency] = Parameter(default=()),
        min_amount: NonNegativeFloat = Parameter(default=0),
        source_payments: list[AnyPayment] = Parameter(default=()),
        target_payments: list[AnyPayment] = Parameter(default=()),
        exchanger_service: FiatAnyCryptoExchangerService = Dependency(),
    ) -> ExchangeRateInResponse:
        filter = FiatAnyCryptoFilter(
            source_params=FiatParams(
                currency=source_currency,
                min_amount=min_amount,
                payments=frozenset(source_payments),
            ),
            target_params=FiatParams(
                currency=target_currency,
                min_amount=0,
                payments=frozenset(target_payments),
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
            source_payments=list(fiat_order.source_order.payments),
            target_payments=list(fiat_order.target_order.payments),
        )
        return response
