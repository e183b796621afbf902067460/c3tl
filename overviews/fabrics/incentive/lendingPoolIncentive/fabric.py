from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.aave.overview import AaveV2LendingPoolIncentiveOverview
from overviews.protocols.geist.overview import GeistLendingPoolIncentiveOverview


class LendingPoolIncentiveOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Lending Incentive Overview handler for {protocol}')
        return overview


lendingPoolIncentiveOverviewFabric = LendingPoolIncentiveOverviewFabric()

lendingPoolIncentiveOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolIncentiveOverview)
lendingPoolIncentiveOverviewFabric.addProduct(protocol='geist', overview=GeistLendingPoolIncentiveOverview)
