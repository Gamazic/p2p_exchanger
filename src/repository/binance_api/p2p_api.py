from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient, codes

from src.repository.binance_api.models import SearchApiParams, SearchApiResponse

__all__ = ["P2PBinanceApi", "P2PBinanceApiError"]


class P2PBinanceApiError(Exception):
    ...


class P2PBinanceApi:
    __URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def __init__(self, client: AsyncClient):
        self.__client = client

    async def search(self, search_params: SearchApiParams) -> SearchApiResponse:
        json_payload = jsonable_encoder(search_params, by_alias=True, exclude_none=True)
        response = await self.__client.post(self.__URL, json=json_payload)
        if response.status_code != codes.OK:
            raise P2PBinanceApiError(
                f"Something wrong with P2PBinanceApi, expected status OK, "
                f"got {response.status_code}, response content: {response.content!r}"
            )
        return SearchApiResponse.parse_raw(response.content)
