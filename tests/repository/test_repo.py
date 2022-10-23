from datetime import datetime

import pytest
from httpx import AsyncClient, Request, Response

from src.domain.p2p import P2PFilter, P2POrder
from src.repository.binance_api.models import (CryptoCurrency, FiatCurrency,
                                               KztPayment, P2PTradeType,
                                               RuPayment)
from src.repository.binance_api.p2p_api import (P2PBinanceApi,
                                                P2PBinanceApiError)
from src.repository.p2p_binance_repo import P2PBinanceRepository
from tests.repository.test_models import (  # type: ignore
    EXAMPLE_SEARCH_API_ARG, EXAMPLE_SEARCH_API_RETURN)


class TestP2PBinanceApi:
    @pytest.fixture()
    async def client(self):
        async with AsyncClient() as client:
            yield client

    async def test_search_api(self, client):
        # TODO возможно интеграционные тесты стоит перенести
        # отдельный модуль.
        p2p_api = P2PBinanceApi(client)
        response = await p2p_api.search(EXAMPLE_SEARCH_API_ARG)
        assert response.success is True

    @pytest.fixture()
    def client_not_connected_stub(self):
        class ClientStub:
            async def post(self, *args, **kwargs):
                return Response(
                    status_code=404, request=Request("POST", "https://test.ru")
                )

        return ClientStub()

    async def test_if_connection_troubles(self, client_not_connected_stub):
        p2p_api = P2PBinanceApi(client_not_connected_stub)
        with pytest.raises(P2PBinanceApiError):
            await p2p_api.search(EXAMPLE_SEARCH_API_ARG)


EXAMPLE_P2PRepo_FIND_FILTER_KZT = P2PFilter(
    source_currency=CryptoCurrency.USDT,
    target_currency=FiatCurrency.KZT,
    min_amount=0,
    payments=[KztPayment.KaspiBank],
)
EXAMPLE_P2PRepo_FIND_RETURN_KZT = P2POrder(
    source_currency=CryptoCurrency.USDT,
    target_currency=FiatCurrency.KZT,
    price=512.23,
    amount=5001.0,
    trade_type=P2PTradeType.SELL,
    payments=[KztPayment.KaspiBank],
    datetime=datetime.now(),
)
EXAMPLE_P2PRepo_FIND_FILTER_RUB = P2PFilter(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.USDT,
    min_amount=0,
    payments=[RuPayment.TinkoffNew],
)
EXAMPLE_P2PRepo_FIND_RETURN_RUB = P2POrder(
    source_currency=FiatCurrency.RUB,
    target_currency=CryptoCurrency.USDT,
    price=61.82,
    amount=5001.0,
    trade_type=P2PTradeType.BUY,
    payments=[RuPayment.TinkoffNew],
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
        repo = P2PBinanceRepository(p2p_binance_api)
        result = await repo.find(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result[0].dict(
            exclude={"datetime"}
        ) == EXAMPLE_P2PRepo_FIND_RETURN_RUB.dict(exclude={"datetime"})
