from datetime import datetime

from src.domain.p2p import P2PFilter, P2POrder
from src.repository.binance_api.models import (FiatCurrency, P2PTradeType,
                                               SearchApiParams)
from src.repository.binance_api.p2p_api import P2PBinanceApi


class P2PBinanceRepository:
    def __init__(self, binance_api: P2PBinanceApi):
        self.__binance_api = binance_api

    async def find(self, filter: P2PFilter) -> list[P2POrder]:
        source_is_fiat = filter.source_currency in FiatCurrency
        if source_is_fiat:
            asset = filter.target_currency
            fiat = filter.source_currency
            trade_type = P2PTradeType.BUY
        else:
            asset = filter.source_currency
            fiat = filter.target_currency
            trade_type = P2PTradeType.SELL

        search_params = SearchApiParams(
            asset=asset,
            fiat=fiat,
            trade_type=trade_type,
            pay_types=filter.payments,
            trans_amount=filter.min_amount,
        )
        dt = datetime.now()
        result = await self.__binance_api.search(search_params)
        p2p_orders = []
        for binance_p2p_order in result.data:
            payments = [tm.identifier for tm in binance_p2p_order.adv.trade_methods]
            order = P2POrder(
                source_currency=filter.source_currency,
                target_currency=filter.target_currency,
                price=binance_p2p_order.adv.price,
                amount=binance_p2p_order.adv.max_single_trans_amount,
                trade_type=trade_type,
                payments=payments,
                datetime=dt,
            )
            p2p_orders.append(order)
        return p2p_orders
