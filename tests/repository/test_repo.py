import pytest
from httpx import AsyncClient, Request, Response

from src.repository.binance_api.p2p_api import (P2PBinanceApi,
                                                P2PBinanceApiError)
from tests.repository.test_models import \
    EXAMPLE_SEARCH_API_PARAMS  # type: ignore


class TestP2PBinanceRepo:
    @pytest.fixture()
    async def client(self):
        async with AsyncClient() as client:
            yield client

    async def test_search_api(self, client):
        p2p_api = P2PBinanceApi(client)
        response = await p2p_api.search(EXAMPLE_SEARCH_API_PARAMS)
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
            await p2p_api.search(EXAMPLE_SEARCH_API_PARAMS)
