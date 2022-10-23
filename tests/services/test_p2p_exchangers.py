import pytest

from src.services.exchangers import P2PExhcnagerService
from tests.repository.test_repo import (EXAMPLE_P2PRepo_FIND_FILTER,  # type: ignore
                                        EXAMPLE_P2PRepo_FIND_RETURN)


class TestP2PExchanger:
    @pytest.fixture()
    def repo_stub(self):
        class RepoStub:
            async def find(self, *args, **kwargs):
                return [EXAMPLE_P2PRepo_FIND_RETURN]

        return RepoStub()

    async def test_find_best_price(self, repo_stub):
        service = P2PExhcnagerService(repo_stub)
        result = await service.find_best_price(EXAMPLE_P2PRepo_FIND_FILTER)
        assert result == EXAMPLE_P2PRepo_FIND_RETURN
