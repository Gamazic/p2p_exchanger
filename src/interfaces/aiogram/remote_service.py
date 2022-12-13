from datetime import datetime
from functools import cached_property
from typing import TypedDict

from httpx import AsyncClient, QueryParams


class SearchFilter(QueryParams):
    source_currency: str
    target_currency: str
    intermediate_cryptos: list[str]
    min_amount: float
    source_payments: list[str]
    target_payments: list[str]


class Order(TypedDict):
    source_currency: str
    target_currency: str
    exchange_rate: float
    source_amount: float
    source_payments: list[str]
    target_payments: list[str]
    acquisition_time: datetime
    intermediate_crypto: str


class ExchangerService:
    @cached_property
    def exchange_rate_url(self):
        return "/best_exchange_rate"

    def __init__(self, exchanger_client: AsyncClient):
        """
        :param exchanger_client: Should contain base url of exchanger api
        """
        self.__client = exchanger_client

    async def get_best_exchange_rate(self, search_filter: SearchFilter) -> Order:
        response = await self.__client.get(self.exchange_rate_url, params=search_filter)
        response.raise_for_status()
        return response.json()
