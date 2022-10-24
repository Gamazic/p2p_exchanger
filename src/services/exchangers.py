from typing import Generator, Protocol

from src.domain.fiat import (FiatAnyCryptoFilter, FiatFixedCryptoFilter,
                             FiatOrder)
from src.domain.p2p import P2PFilter, P2POrder
from src.repository.binance_api.models import CryptoCurrency
from src.repository.p2p_binance_repo import IP2PRepo


class IExchanger(Protocol):
    async def find_best_price(self, filter):
        raise NotImplementedError()


class P2PExhcnagerService(IExchanger):
    def __init__(self, p2p_repo: IP2PRepo):
        self.__p2p_repo = p2p_repo

    async def find_best_price(self, filter: P2PFilter) -> P2POrder:
        orders = await self.__p2p_repo.find(filter)
        return max(
            orders, key=lambda o: o.price
        )  # TODO if orders are ordered, than take just first el


class FiatFixedCryptoExchangerService(IExchanger):
    def __init__(self, p2p_exchanger: P2PExhcnagerService):
        self.__p2p_exchanger = p2p_exchanger

    async def find_best_price(self, filter: FiatFixedCryptoFilter) -> FiatOrder:
        source_order = await self.__get_source_order(filter)
        target_order = await self.__get_target_order(filter)
        price = target_order.price / source_order.price
        fiat_order = FiatOrder(
            source_order=source_order,
            target_order=target_order,
            price=price,
        )
        return fiat_order

    async def __get_source_order(self, filter: FiatFixedCryptoFilter) -> P2POrder:
        source_p2p_filter = P2PFilter(
            source_currency=filter.source_params.currency,
            target_currency=filter.intermediate_crypto,
            min_amount=filter.source_params.min_amount,
            payments=list(filter.source_params.payments),
        )
        return await self.__p2p_exchanger.find_best_price(source_p2p_filter)

    async def __get_target_order(self, filter: FiatFixedCryptoFilter) -> P2POrder:
        target_p2p_filter = P2PFilter(
            source_currency=filter.intermediate_crypto,
            target_currency=filter.target_params.currency,
            min_amount=filter.target_params.min_amount,
            payments=list(filter.target_params.payments),
        )
        return await self.__p2p_exchanger.find_best_price(target_p2p_filter)


class FiatAnyCryptoExchangerService(IExchanger):
    def __init__(self, fiat_exchanger: FiatFixedCryptoExchangerService):
        self.__fiat_exhcnager = fiat_exchanger

    async def find_best_price(self, filter: FiatAnyCryptoFilter) -> FiatOrder:
        orders = await self.__find(filter)
        return max(orders, key=lambda order: order.price)

    async def __find(self, filter: FiatAnyCryptoFilter):
        orders = []
        cryptos_iterator = filter.intermediate_cryptos or CryptoCurrency
        for crypto in cryptos_iterator:
            fiat_fixed_crypto_filter = FiatFixedCryptoFilter(
                source_params=filter.source_params,
                target_params=filter.target_params,
                intermediate_crypto=crypto,
            )
            fiat_fixed_crypto_order = await self.__fiat_exhcnager.find_best_price(
                fiat_fixed_crypto_filter
            )
            orders.append(fiat_fixed_crypto_order)
        return orders
