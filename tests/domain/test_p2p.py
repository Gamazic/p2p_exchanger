from datetime import datetime

import pytest

from src.domain.p2p import P2POrder, P2PSameCurrencyTypeError, P2PTradeTypeError, P2PFilter
from src.repository.binance_api.models import (CryptoCurrency, FiatCurrency,
                                               P2PTradeType)


class TestP2POrder:
    def test_correct_order(self):
        P2POrder(
            source_currency=FiatCurrency.RUB,
            target_currency=CryptoCurrency.BTC,
            price=0,
            amount=0,
            trade_type=P2PTradeType.BUY,
            payments=[],
            datetime=datetime.now(),
        )

    def test_same_currency(self):
        with pytest.raises(P2PSameCurrencyTypeError):
            P2POrder(
                source_currency=FiatCurrency.RUB,
                target_currency=FiatCurrency.KZT,
                price=0,
                amount=0,
                trade_type=P2PTradeType.BUY,
                payments=[],
                datetime=datetime.now(),
            )
        with pytest.raises(P2PSameCurrencyTypeError):
            P2POrder(
                source_currency=CryptoCurrency.USDT,
                target_currency=CryptoCurrency.BTC,
                price=0,
                amount=0,
                trade_type=P2PTradeType.BUY,
                payments=[],
                datetime=datetime.now(),
            )

    def test_bad_trade_type(self):
        with pytest.raises(P2PTradeTypeError):
            P2POrder(
                source_currency=FiatCurrency.RUB,
                target_currency=CryptoCurrency.USDT,
                price=0,
                amount=0,
                trade_type=P2PTradeType.SELL,
                payments=[],
                datetime=datetime.now(),
            )
        with pytest.raises(P2PTradeTypeError):
            P2POrder(
                source_currency=CryptoCurrency.USDT,
                target_currency=FiatCurrency.RUB,
                price=0,
                amount=0,
                trade_type=P2PTradeType.BUY,
                payments=[],
                datetime=datetime.now(),
            )


class TestP2PFilter:
    def test_correct_filter(self):
        P2PFilter(
            source_currency=FiatCurrency.RUB,
            target_currency=CryptoCurrency.BTC,
            min_amount=0,
            payments=[]
        )

    def test_currencies(self):
        with pytest.raises(P2PSameCurrencyTypeError):
            P2PFilter(
                source_currency=FiatCurrency.RUB,
                target_currency=FiatCurrency.KZT,
                min_amount=0,
                payments=[]
            )