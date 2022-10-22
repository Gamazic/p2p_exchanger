from httpx import AsyncClient

from src.repository.binance_api.models import (SearchApiParams,
                                               SearchApiResponse)


class P2PBinanceApiError(Exception):
    ...


class P2PBinanceApi:
    __URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def __init__(self, client: AsyncClient):
        self.__client = client

    async def search(self, search_params: SearchApiParams) -> SearchApiResponse:
        json_payload = search_params.dict(by_alias=True, exclude_none=True)
        response = await self.__client.post(self.__URL, json=json_payload)
        if response.status_code != 200:
            raise P2PBinanceApiError("Something wrong with P2PBinanceApi")
        response_json = response.json()
        return SearchApiResponse.parse_obj(response_json)
