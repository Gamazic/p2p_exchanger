from asyncio import sleep
from datetime import datetime, timedelta

import pytest
from src.domain.p2p import P2PFilter, P2POrder
from src.repository.binance_api.models import CryptoCurrency, FiatCurrency, KztPayment, P2PTradeType, RubPayment
from src.repository.p2p_binance_repo import CachedP2PBinanceRepo, P2PBinanceRepo

from tests.repository.test_models import (
    EXAMPLE_2_SEARCH_API_ARG,
    EXAMPLE_2_SEARCH_API_RETURN,
    EXAMPLE_2_SEARCH_API_RETURN_2,
    EXAMPLE_SEARCH_API_ARG,
    EXAMPLE_SEARCH_API_RETURN,
    EXAMPLE_SEARCH_API_RETURN_2,
)

EXAMPLE_P2PRepo_FIND_FILTER_KZT = P2PFilter(
    source_currency=CryptoCurrency.USDT,
    target_currency=FiatCurrency.KZT,
    min_amount=0,
    payments=frozenset({KztPayment.KaspiBank}),
)
EXAMPLE_P2PRepo_FIND_RETURN_KZT = P2POrder(
    source_currency=CryptoCurrency.USDT,
    target_currency=FiatCurrency.KZT,
    price=512.23,
    amount=5001.0,
    trade_type=P2PTradeType.SELL,
    payments={KztPayment.KaspiBank},
    datetime=datetime.now(),
)
EXAMPLE_P2PRepo_FIND_FILTER_RUB = P2PFilter(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.USDT,
    min_amount=0,
    payments=frozenset({RubPayment.TinkoffNew}),
)
EXAMPLE_P2PRepo_FIND_RETURN_RUB = P2POrder(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.USDT,
    price=61.82,
    amount=5001.0,
    trade_type=P2PTradeType.BUY,
    payments={RubPayment.TinkoffNew},
    datetime=datetime.now(),
)


class TestP2PBinanceRepository:
    @pytest.fixture()
    def p2p_binance_api(self):
        class ApiStub:
            async def search(self, *args, **kwargs):
                return EXAMPLE_SEARCH_API_RETURN

        return ApiStub()

    async def test_find(self, p2p_binance_api):
        repo = P2PBinanceRepo(p2p_binance_api)
        result = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result[0].dict(exclude={"datetime"}) == EXAMPLE_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})


EXAMPLE_2_P2PRepo_FIND_FILTER_RUB = P2PFilter(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.BTC,
    min_amount=0,
    payments=frozenset({RubPayment.TinkoffNew}),
)
EXAMPLE_2_P2PRepo_FIND_RETURN_RUB = P2POrder(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.BTC,
    price=228,
    amount=5001.0,
    trade_type=P2PTradeType.BUY,
    payments={RubPayment.TinkoffNew},
    datetime=datetime.now(),
)


class TestCachedP2PRepo:
    @pytest.fixture()
    def p2p_binance_api(self):
        class ApiStub:
            def __init__(self):
                self.e1_called = False
                self.e2_called = False

            async def search(self, filter):
                if filter == EXAMPLE_SEARCH_API_ARG:
                    if not self.e1_called:
                        self.e1_called = True
                        return EXAMPLE_SEARCH_API_RETURN
                    else:
                        return EXAMPLE_SEARCH_API_RETURN_2
                elif filter == EXAMPLE_2_SEARCH_API_ARG:
                    if not self.e2_called:
                        self.e2_called = True
                        return EXAMPLE_2_SEARCH_API_RETURN
                    else:
                        return EXAMPLE_2_SEARCH_API_RETURN_2
                else:
                    raise NotImplementedError

        return ApiStub()

    async def test_find(self, p2p_binance_api):
        CachedP2PBinanceRepo.TTL = 0.5
        repo = CachedP2PBinanceRepo(p2p_binance_api)

        exec_start = datetime.now()
        result_e1_1 = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result_e1_1[0].dict(exclude={"datetime"}) == EXAMPLE_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
        result_e1_2 = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result_e1_2[0].dict(exclude={"datetime"}) == EXAMPLE_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
        result_e2_1 = await repo.find(EXAMPLE_2_P2PRepo_FIND_FILTER_RUB)
        assert result_e2_1[0].dict(exclude={"datetime"}) == EXAMPLE_2_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
        result_e2_2 = await repo.find(EXAMPLE_2_P2PRepo_FIND_FILTER_RUB)
        assert result_e2_2[0].dict(exclude={"datetime"}) == EXAMPLE_2_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
        exec_time = datetime.now() - exec_start
        if exec_time > timedelta(seconds=repo.TTL):
            raise RuntimeError("Cannot test it, because execution longer than ttl")

        await sleep(repo.TTL)
        result_e1_3 = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result_e1_3[0].dict(exclude={"datetime"}) != EXAMPLE_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
        result_e2_3 = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result_e2_3[0].dict(exclude={"datetime"}) != EXAMPLE_2_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
