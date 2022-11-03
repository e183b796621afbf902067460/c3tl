from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.convex.overview import ConvexStakingPoolAllocationOverview
from overviews.protocols.curve.overview import CurveStakingPoolAllocationOverview


class StakingPoolAllocationOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Staking Allocation Overview handler for {protocol}')
        return overview


stakingPoolAllocationOverviewFabric = StakingPoolAllocationOverviewFabric()

stakingPoolAllocationOverviewFabric.addProduct(protocol='convex', overview=ConvexStakingPoolAllocationOverview)
stakingPoolAllocationOverviewFabric.addProduct(protocol='curve', overview=CurveStakingPoolAllocationOverview)
