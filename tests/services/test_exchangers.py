from datetime import datetime

import pytest

from src.domain.fiat import (FiatAnyCryptoFilter, FiatFixedCryptoFilter,
                             FiatOrder, FiatParams)
from src.domain.p2p import P2POrder
from src.repository.binance_api.models import (CryptoCurrency, FiatCurrency,
                                               KztPayment, P2PTradeType,
                                               RubPayment)
from src.services.exchangers import (FiatAnyCryptoExchangerService,
                                     FiatFixedCryptoExchangerService,
                                     P2PExchangerService)
from tests.repository.test_repo import (  # type: ignore
    EXAMPLE_P2PRepo_FIND_FILTER_KZT, EXAMPLE_P2PRepo_FIND_FILTER_RUB,
    EXAMPLE_P2PRepo_FIND_RETURN_KZT, EXAMPLE_P2PRepo_FIND_RETURN_RUB)


class TestP2PExchanger:
    @pytest.fixture()
    def repo_stub(self):
        class RepoStub:
            async def find(self, *args, **kwargs):
                return [EXAMPLE_P2PRepo_FIND_RETURN_RUB]

        return RepoStub()

    async def test_find_best_price(self, repo_stub):
        service = P2PExchangerService(repo_stub)
        result = await service.find_best_price(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result == EXAMPLE_P2PRepo_FIND_RETURN_RUB


EXAMPLE_FiatExchanger_USDT_FIND_FILTER = FiatFixedCryptoFilter(
    source_params=FiatParams(
        currency=FiatCurrency.RUB,
        min_amount=0,
        payments=frozenset({RubPayment.TinkoffNew}),
    ),
    target_params=FiatParams(
        currency=FiatCurrency.KZT,
        min_amount=0,
        payments=frozenset({KztPayment.KaspiBank}),
    ),
    intermediate_crypto=CryptoCurrency.USDT,
)
EXAMPLE_FiatExchanger_BTC_FIND_FILTER = FiatFixedCryptoFilter(
    source_params=FiatParams(
        currency=FiatCurrency.RUB,
        min_amount=0,
        payments=frozenset({RubPayment.TinkoffNew}),
    ),
    target_params=FiatParams(
        currency=FiatCurrency.KZT,
        min_amount=0,
        payments=frozenset({KztPayment.KaspiBank}),
    ),
    intermediate_crypto=CryptoCurrency.BTC,
)
EXAMPLE_FiatExchanger_USDT_FIND_RETURN = FiatOrder(
    source_order=EXAMPLE_P2PRepo_FIND_RETURN_RUB,
    target_order=EXAMPLE_P2PRepo_FIND_RETURN_KZT,
    price=EXAMPLE_P2PRepo_FIND_RETURN_KZT.price / EXAMPLE_P2PRepo_FIND_RETURN_RUB.price,
)
EXAMPLE_FiatExchanger_BTC_FIND_RETURN = FiatOrder(
    source_order=P2POrder(
        source_currency=FiatCurrency.RUB,
        target_currency=CryptoCurrency.BTC,
        price=30.12,
        amount=5001.0,
        trade_type=P2PTradeType.BUY,
        payments={RubPayment.TinkoffNew},
        datetime=datetime.now(),
    ),
    target_order=P2POrder(
        source_currency=CryptoCurrency.BTC,
        target_currency=FiatCurrency.KZT,
        price=512.23,
        amount=5001.0,
        trade_type=P2PTradeType.SELL,
        payments={KztPayment.KaspiBank},
        datetime=datetime.now(),
    ),
    price=512.23 / 30.12,
)


class TestFiatFixedCryptoExchanger:
    @pytest.fixture()
    def p2p_exchanger_stub(self):
        class P2PExchangerStub:
            async def find_best_price(self, filter):
                if filter == EXAMPLE_P2PRepo_FIND_FILTER_RUB:
                    return EXAMPLE_P2PRepo_FIND_RETURN_RUB
                elif filter == EXAMPLE_P2PRepo_FIND_FILTER_KZT:
                    return EXAMPLE_P2PRepo_FIND_RETURN_KZT
                else:
                    raise NotImplementedError()

        return P2PExchangerStub()

    async def test_find_best_price(self, p2p_exchanger_stub):
        service = FiatFixedCryptoExchangerService(p2p_exchanger_stub)
        result = await service.find_best_price(EXAMPLE_FiatExchanger_USDT_FIND_FILTER)
        assert result.price == (
            EXAMPLE_P2PRepo_FIND_RETURN_KZT.price
            / EXAMPLE_P2PRepo_FIND_RETURN_RUB.price
        )
        assert result == EXAMPLE_FiatExchanger_USDT_FIND_RETURN


EXAMPLE_FiatAnyCryptoExchanger_FIND_FILTER = FiatAnyCryptoFilter(
    source_params=FiatParams(
        currency=FiatCurrency.RUB,
        min_amount=0,
        payments=frozenset({RubPayment.TinkoffNew}),
    ),
    target_params=FiatParams(
        currency=FiatCurrency.KZT,
        min_amount=0,
        payments=frozenset({KztPayment.KaspiBank}),
    ),
    intermediate_cryptos=[CryptoCurrency.USDT, CryptoCurrency.BTC],
)


class TestFiatAnyCryptoExchanger:
    @pytest.fixture()
    def fiat_exchanger_stub(self):
        class FiatFixedCryptoExchangerStub:
            async def find_best_price(self, filter):
                if filter == EXAMPLE_FiatExchanger_BTC_FIND_FILTER:
                    return EXAMPLE_FiatExchanger_BTC_FIND_RETURN
                elif filter == EXAMPLE_FiatExchanger_USDT_FIND_FILTER:
                    return EXAMPLE_FiatExchanger_USDT_FIND_RETURN
                else:
                    raise NotImplementedError()

        return FiatFixedCryptoExchangerStub()

    async def test_find_best_price(self, fiat_exchanger_stub):
        service = FiatAnyCryptoExchangerService(fiat_exchanger_stub)
        result = await service.find_best_price(
            EXAMPLE_FiatAnyCryptoExchanger_FIND_FILTER
        )
        assert result == EXAMPLE_FiatExchanger_BTC_FIND_RETURN
