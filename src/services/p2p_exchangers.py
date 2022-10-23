from src.domain.p2p import P2PFilter, P2POrder
from src.repository.p2p_binance_repo import IP2PRepo


class P2PExhcnagerService:
    def __init__(self, p2p_repo: IP2PRepo):
        self.__p2p_repo = p2p_repo

    async def find_best_price(self, filter: P2PFilter) -> P2POrder:
        orders = await self.__p2p_repo.find(filter)
        return max(
            orders, key=lambda o: o.price
        )  # TODO if orders are ordered, than take just first el
