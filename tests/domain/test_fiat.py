from datetime import datetime

import pytest

from src.domain.fiat import (BadP2POrderTypeError, DifferentP2PCryptoError,
                             FiatFixedCryptoFilter, FiatOrder, FiatParams,
                             SameFiatCurrencyError)
from src.domain.p2p import P2POrder
from src.repository.binance_api.models import (AnyPayment, CryptoCurrency,
                                               FiatCurrency, KztPayment,
                                               P2PTradeType,
                                               PaymentDoesntMatchCurrencyError,
                                               RuPayment)


class TestFiatParams:
    @pytest.mark.parametrize(
        "currency,payments,is_wrong",
        [
            (FiatCurrency.RUB, [KztPayment.KaspiBank, KztPayment.KaspiBank], True),
            (FiatCurrency.RUB, [KztPayment.KaspiBank, RuPayment.RosBankNew], True),
            (FiatCurrency.RUB, [RuPayment.TinkoffNew, RuPayment.RosBankNew], False),
            (FiatCurrency.RUB, [RuPayment.RosBankNew, RuPayment.RosBankNew], False),
        ],
    )
    def test(self, currency, payments, is_wrong):
        if is_wrong:
            with pytest.raises(PaymentDoesntMatchCurrencyError):
                FiatParams(currency=currency, min_amount=10, payments=payments)
        else:
            FiatParams(currency=currency, min_amount=10, payments=payments)


class TestFiatFixedCryptoFilter:
    def test_correct(self):
        FiatFixedCryptoFilter(
            source_params=FiatParams(
                currency=FiatCurrency.RUB, min_amount=0, payments=[]
            ),
            target_params=FiatParams(
                currency=FiatCurrency.KZT, min_amount=0, payments=[]
            ),
            intermediate_crypto=CryptoCurrency.USDT,
        )

    def test_same_currency(self):
        with pytest.raises(SameFiatCurrencyError):
            FiatFixedCryptoFilter(
                source_params=FiatParams(
                    currency=FiatCurrency.RUB, min_amount=0, payments=[]
                ),
                target_params=FiatParams(
                    currency=FiatCurrency.RUB, min_amount=0, payments=[]
                ),
                intermediate_crypto=CryptoCurrency.USDT,
            )


class TestFiatOrder:
    def test_correct(self):
        FiatOrder(
            source_order=P2POrder(
                source_currency=FiatCurrency.RUB,
                target_currency=CryptoCurrency.USDT,
                price=50,
                amount=100,
                trade_type=P2PTradeType.BUY,
                payments=[RuPayment.TinkoffNew, RuPayment.RaiffeisenBank],
                datetime=datetime(2021, 1, 1),
            ),
            target_order=P2POrder(
                source_currency=CryptoCurrency.USDT,
                target_currency=FiatCurrency.KZT,
                price=100,
                amount=100,
                trade_type=P2PTradeType.SELL,
                payments=[KztPayment.KaspiBank],
                datetime=datetime(2021, 1, 1),
            ),
            price=2,
        )

    def test_same_fiat(self):
        with pytest.raises(SameFiatCurrencyError):
            FiatOrder(
                source_order=P2POrder(
                    source_currency=FiatCurrency.RUB,
                    target_currency=CryptoCurrency.USDT,
                    price=50,
                    amount=100,
                    trade_type=P2PTradeType.BUY,
                    payments=[RuPayment.TinkoffNew, RuPayment.RaiffeisenBank],
                    datetime=datetime(2021, 1, 1),
                ),
                target_order=P2POrder(
                    source_currency=CryptoCurrency.USDT,
                    target_currency=FiatCurrency.RUB,
                    price=100,
                    amount=100,
                    trade_type=P2PTradeType.SELL,
                    payments=[RuPayment.TinkoffNew],
                    datetime=datetime(2021, 1, 1),
                ),
                price=2,
            )

    def test_different_crypto(self):
        with pytest.raises(DifferentP2PCryptoError):
            FiatOrder(
                source_order=P2POrder(
                    source_currency=FiatCurrency.RUB,
                    target_currency=CryptoCurrency.USDT,
                    price=50,
                    amount=100,
                    trade_type=P2PTradeType.BUY,
                    payments=[RuPayment.TinkoffNew, RuPayment.RaiffeisenBank],
                    datetime=datetime(2021, 1, 1),
                ),
                target_order=P2POrder(
                    source_currency=CryptoCurrency.BTC,
                    target_currency=FiatCurrency.KZT,
                    price=100,
                    amount=100,
                    trade_type=P2PTradeType.SELL,
                    payments=[KztPayment.KaspiBank],
                    datetime=datetime(2021, 1, 1),
                ),
                price=2,
            )

    def test_order_types(self):
        with pytest.raises(BadP2POrderTypeError):
            FiatOrder(
                source_order=P2POrder(
                    source_currency=CryptoCurrency.BTC,
                    target_currency=FiatCurrency.RUB,
                    price=50,
                    amount=100,
                    trade_type=P2PTradeType.SELL,
                    payments=[RuPayment.TinkoffNew, RuPayment.RaiffeisenBank],
                    datetime=datetime(2021, 1, 1),
                ),
                target_order=P2POrder(
                    source_currency=CryptoCurrency.USDT,
                    target_currency=FiatCurrency.KZT,
                    price=100,
                    amount=100,
                    trade_type=P2PTradeType.SELL,
                    payments=[KztPayment.KaspiBank],
                    datetime=datetime(2021, 1, 1),
                ),
                price=2,
            )
