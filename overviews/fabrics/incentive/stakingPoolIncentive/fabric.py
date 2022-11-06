from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.convex.overview import ConvexStakingPoolIncentiveOverview


class StakingPoolIncentiveOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Staking Incentive Overview handler for {protocol}')
        return overview


stakingPoolIncentiveOverviewFabric = StakingPoolIncentiveOverviewFabric()

stakingPoolIncentiveOverviewFabric.addProduct(protocol='convex', overview=ConvexStakingPoolIncentiveOverview)
