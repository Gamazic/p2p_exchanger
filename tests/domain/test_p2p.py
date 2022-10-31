from datetime import datetime

import pytest

from src.domain.p2p import (P2PFilter, P2POrder, P2PSameCurrencyTypeError,
                            P2PTradeTypeError)
from src.repository.binance_api.models import (CryptoCurrency, FiatCurrency,
                                               KztPayment, P2PTradeType,
                                               PaymentDoesntMatchCurrencyError,
                                               RubPayment)


class TestP2POrder:
    def test_correct_order(self):
        P2POrder(
            source_currency=FiatCurrency.RUB,
            target_currency=CryptoCurrency.BTC,
            price=0,
            amount=0,
            trade_type=P2PTradeType.BUY,
            payments=set(),
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
                payments=set(),
                datetime=datetime.now(),
            )
        with pytest.raises(P2PSameCurrencyTypeError):
            P2POrder(
                source_currency=CryptoCurrency.USDT,
                target_currency=CryptoCurrency.BTC,
                price=0,
                amount=0,
                trade_type=P2PTradeType.BUY,
                payments=set(),
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
                payments=set(),
                datetime=datetime.now(),
            )
        with pytest.raises(P2PTradeTypeError):
            P2POrder(
                source_currency=CryptoCurrency.USDT,
                target_currency=FiatCurrency.RUB,
                price=0,
                amount=0,
                trade_type=P2PTradeType.BUY,
                payments=set(),
                datetime=datetime.now(),
            )


class TestP2PFilter:
    def test_correct_filter(self):
        P2PFilter(
            source_currency=FiatCurrency.RUB,
            target_currency=CryptoCurrency.BTC,
            min_amount=0,
            payments=frozenset(),
        )

    def test_currencies(self):
        with pytest.raises(P2PSameCurrencyTypeError):
            P2PFilter(
                source_currency=FiatCurrency.RUB,
                target_currency=FiatCurrency.KZT,
                min_amount=0,
                payments=frozenset(),
            )

    def test_payments(self):
        with pytest.raises(PaymentDoesntMatchCurrencyError):
            P2PFilter(
                source_currency=FiatCurrency.RUB,
                target_currency=CryptoCurrency.USDT,
                min_amount=0,
                payments=frozenset({KztPayment.KaspiBank}),
            )
        P2PFilter(
            source_currency=FiatCurrency.RUB,
            target_currency=CryptoCurrency.USDT,
            min_amount=0,
            payments=frozenset({RubPayment.TinkoffNew, RubPayment.RaiffeisenBank}),
        )
        P2PFilter(
            source_currency=CryptoCurrency.USDT,
            target_currency=FiatCurrency.KZT,
            min_amount=0,
            payments=frozenset({KztPayment.KaspiBank}),
        )
