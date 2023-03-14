from functools import cache

from httpx import AsyncClient

from src.interfaces.starlite.logger import log_request, log_response
from src.repository.binance_api.p2p_api import P2PBinanceApi
from src.repository.p2p_binance_repo import CachedP2PBinanceRepo
from src.services.exchangers import FiatAnyCryptoExchangerService, FiatFixedCryptoExchangerService, P2PExchangerService

__all__ = ["get_exchanger"]


@cache
def get_exchanger():
    exchanger_service = FiatAnyCryptoExchangerService(
        FiatFixedCryptoExchangerService(
            P2PExchangerService(
                CachedP2PBinanceRepo(
                    P2PBinanceApi(
                        AsyncClient(
                            event_hooks={
                                "request": [log_request],
                                "response": [log_response],
                            }
                        )
                    )
                )
            )
        )
    )
    return exchanger_service
