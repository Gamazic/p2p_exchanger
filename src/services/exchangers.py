import asyncio
from typing import Protocol

from src.domain.fiat import FiatAnyCryptoFilter, FiatFixedCryptoFilter, FiatOrder
from src.domain.p2p import P2PFilter, P2POrder
from src.repository.binance_api.models import CryptoCurrency
from src.repository.p2p_binance_repo import P2PRepoProto

__all__ = ["FiatAnyCryptoExchangerService", "FiatFixedCryptoExchangerService", "IExchanger", "P2PExchangerService"]


class IExchanger(Protocol):
    async def find_best_price(self, filter):
        raise NotImplementedError()


class P2PExchangerService(IExchanger):
    def __init__(self, p2p_repo: P2PRepoProto):
        self.__p2p_repo = p2p_repo

    async def find_best_price(self, filter: P2PFilter) -> P2POrder:
        orders = await self.__p2p_repo.find(filter)
        return max(orders, key=lambda o: o.price)  # TODO if orders are ordered, than take just first el


class FiatFixedCryptoExchangerService(IExchanger):
    def __init__(self, p2p_exchanger: P2PExchangerService):
        self.__p2p_exchanger = p2p_exchanger

    async def find_best_price(self, filter: FiatFixedCryptoFilter) -> FiatOrder:
        source_order_coro = self.__get_source_order(filter)
        target_order_coro = self.__get_target_order(filter)
        source_order, target_order = await asyncio.gather(source_order_coro, target_order_coro)
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
            payments=filter.source_params.payments,
        )
        return await self.__p2p_exchanger.find_best_price(source_p2p_filter)

    async def __get_target_order(self, filter: FiatFixedCryptoFilter) -> P2POrder:
        target_p2p_filter = P2PFilter(
            source_currency=filter.intermediate_crypto,
            target_currency=filter.target_params.currency,
            min_amount=filter.target_params.min_amount,
            payments=filter.target_params.payments,
        )
        return await self.__p2p_exchanger.find_best_price(target_p2p_filter)


class FiatAnyCryptoExchangerService(IExchanger):
    def __init__(self, fiat_exchanger: FiatFixedCryptoExchangerService):
        self.__fiat_exchanger = fiat_exchanger

    async def find_best_price(self, filter: FiatAnyCryptoFilter) -> FiatOrder:
        orders = await self.__find(filter)
        return max(orders, key=lambda order: order.price)

    async def __find(self, filter: FiatAnyCryptoFilter):
        cryptos_iterator = filter.intermediate_cryptos or CryptoCurrency
        fiat_fixed_crypto_order_coros = []
        for crypto in cryptos_iterator:
            fiat_fixed_crypto_filter = FiatFixedCryptoFilter(
                source_params=filter.source_params,
                target_params=filter.target_params,
                intermediate_crypto=crypto,
            )
            fiat_fixed_crypto_order_coros.append(self.__fiat_exchanger.find_best_price(fiat_fixed_crypto_filter))
        orders = await asyncio.gather(*fiat_fixed_crypto_order_coros)
        return orders
