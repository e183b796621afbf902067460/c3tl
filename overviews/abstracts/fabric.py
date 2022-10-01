from head.interfaces.abstracts.interface import IAbstractFabric
from head.interfaces.fabrics.interface import IConcreteFabric

from overviews.fabrics.dexPool.fabric import dexPoolOverviewFabric
from overviews.fabrics.lendingPool.fabric import lendingPoolOverviewFabric
from overviews.fabrics.stakingPool.fabric import stakingPoolOverviewFabric


class OverviewAbstractFabric(IAbstractFabric):

    def addFabric(self, fabricType: str, fabric: IConcreteFabric) -> None:
        if not self._fabrics.get(fabricType):
            self._fabrics[fabricType]: IConcreteFabric = fabric

    def getFabric(self, fabricType: str) -> IConcreteFabric:
        fabric: IConcreteFabric = self._fabrics.get(fabricType)
        if not fabric:
            raise ValueError(f'Set Fabric for {fabricType} fabric type')
        return fabric


overviewAbstractFabric = OverviewAbstractFabric()

overviewAbstractFabric.addFabric(fabricType='dex-pool-overview', fabric=dexPoolOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='lending-pool-overview', fabric=lendingPoolOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='staking-pool-overview', fabric=stakingPoolOverviewFabric)
