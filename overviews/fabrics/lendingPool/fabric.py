from head.interfaces.overview.builder import IInstrumentOverview

from overviews.fabrics.liquidityPool.fabric import LiquidityPoolOverviewFabric

from overviews.protocols.aave.overview import AaveV2LendingPoolOverview
from overviews.protocols.geist.overview import GeistLendingPoolOverview
from overviews.protocols.sturdy.overview import SturdyLendingPoolOverview


class LendingPoolOverviewFabric(LiquidityPoolOverviewFabric):
    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Lending Overview handler for {protocol}')
        return overview


lendingPoolOverviewFabric = LendingPoolOverviewFabric()

lendingPoolOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolOverview)
lendingPoolOverviewFabric.addProduct(protocol='geist', overview=GeistLendingPoolOverview)
lendingPoolOverviewFabric.addProduct(protocol='sturdy', overview=SturdyLendingPoolOverview)
