import pytest

from src.domain.fiat import FiatFixedCryptoFilter, FiatParams
from src.repository.binance_api.models import (CryptoCurrency, FiatCurrency,
                                               KztPayment, RuPayment)
from src.services.exchangers import (FiatFixedCryptoExchangerService,
                                     P2PExhcnagerService)
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
        service = P2PExhcnagerService(repo_stub)
        result = await service.find_best_price(EXAMPLE_P2PRepo_FIND_FILTER_RUB)
        assert result == EXAMPLE_P2PRepo_FIND_RETURN_RUB


EXAMPLE_FiatExchanger_FIND_FILTER = FiatFixedCryptoFilter(
    source_params=FiatParams(
        currency=FiatCurrency.RUB, min_amount=0, payments={RuPayment.TinkoffNew}
    ),
    target_params=FiatParams(
        currency=FiatCurrency.KZT, min_amount=0, payments={KztPayment.KaspiBank}
    ),
    intermediate_crypto=CryptoCurrency.USDT,
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
        result = await service.find_best_price(EXAMPLE_FiatExchanger_FIND_FILTER)
        assert result.price == (
            EXAMPLE_P2PRepo_FIND_RETURN_KZT.price
            / EXAMPLE_P2PRepo_FIND_RETURN_RUB.price
        )
