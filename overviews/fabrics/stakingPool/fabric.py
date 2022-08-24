from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveStakingPoolOverview
from overviews.protocols.convex.overview import ConvexStakingPoolOverview


class StakingPoolOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Staking Overview handler for {protocol}')
        return overview


stakingPoolOverviewFabric = StakingPoolOverviewFabric()

stakingPoolOverviewFabric.addProduct(protocol='curve', overview=CurveStakingPoolOverview())
stakingPoolOverviewFabric.addProduct(protocol='convex', overview=ConvexStakingPoolOverview())
