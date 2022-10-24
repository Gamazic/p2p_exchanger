"""
DI framework. need to think about framework. I want to try `di` lib.
But now it's fastapi di
"""
from functools import cache

from fastapi import Depends
from httpx import AsyncClient

from src.repository.binance_api.p2p_api import P2PBinanceApi
from src.repository.p2p_binance_repo import P2PBinanceRepository
from src.services.exchangers import (FiatAnyCryptoExchangerService,
                                     FiatFixedCryptoExchangerService,
                                     P2PExhcnagerService)


async def http_client():
    async with AsyncClient() as session:
        yield session


def binance_api(client: AsyncClient = Depends(http_client)):
    return P2PBinanceApi(client)


def p2p_repo(binance_api: P2PBinanceApi = Depends(binance_api)):
    return P2PBinanceRepository(binance_api)


def p2p_exchanger(p2p_repo: P2PBinanceRepository = Depends(p2p_repo)):
    return P2PExhcnagerService(p2p_repo)


def fiat_fixed_crypto_exchanger(
    p2p_exchanger: P2PExhcnagerService = Depends(p2p_exchanger),
):
    return FiatFixedCryptoExchangerService(p2p_exchanger)


def fiat_any_crypto_exchanger(
    fiat_exchanger: FiatFixedCryptoExchangerService = Depends(
        fiat_fixed_crypto_exchanger
    ),
):
    return FiatAnyCryptoExchangerService(fiat_exchanger)
