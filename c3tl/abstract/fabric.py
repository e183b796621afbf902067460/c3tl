from abc import ABC
from typing import final

from c3tl.interfaces.fabric.interface import iFabric

from c3tl.fabrics.whole_market_trades_history.fabric import wholeMarketTradesHistoryFabric
from c3tl.fabrics.account_balances.fabric import accountBalancesFabric
from c3tl.fabrics.account_liquidations.fabric import accountLiquidationsFabric


class C3AbstractFabric(ABC):

    def __init__(self) -> None:
        self._fabrics: dict = dict()

    @final
    def add_fabric(self, fabric_name: str, fabric: iFabric) -> None:
        if not self._fabrics.get(fabric_name):
            self._fabrics[fabric_name] = fabric

    @final
    def get_fabric(self, fabric_name: str) -> iFabric:
        fabric: iFabric = self._fabrics.get(fabric_name)
        if not fabric:
            raise ValueError(f'Set Fabric for {fabric_name} fabric type')
        return fabric


c3Abstract: C3AbstractFabric = C3AbstractFabric()

c3Abstract.add_fabric(fabric_name='whole_market_trades_history', fabric=wholeMarketTradesHistoryFabric)
c3Abstract.add_fabric(fabric_name='account_balances', fabric=accountBalancesFabric)
c3Abstract.add_fabric(fabric_name='account_liquidations', fabric=accountLiquidationsFabric)
