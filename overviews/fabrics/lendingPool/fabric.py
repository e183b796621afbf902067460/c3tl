from head.interfaces.overview.builder import IInstrumentOverview

from overviews.fabrics.liquidityPool.fabric import LiquidityPoolOverviewFabric
from overviews.protocols.aave.overview import AaveV2LendingPoolOverview


class LendingPoolOverviewFabric(LiquidityPoolOverviewFabric):
    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Lending Overview handler for {protocol}')
        return overview


lendingPoolOverviewFabric = LendingPoolOverviewFabric()

lendingPoolOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolOverview())
