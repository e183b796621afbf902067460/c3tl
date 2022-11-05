from head.interfaces.abstracts.interface import IAbstractFabric
from head.interfaces.fabrics.interface import IConcreteFabric

from overviews.fabrics.borrow.lendingPoolBorrow.fabric import lendingPoolBorrowOverviewFabric

from overviews.fabrics.pool.dexPool.fabric import dexPoolOverviewFabric
from overviews.fabrics.pool.lendingPool.fabric import lendingPoolOverviewFabric
from overviews.fabrics.pool.stakingPool.fabric import stakingPoolOverviewFabric
from overviews.fabrics.pool.farmingPool.fabric import farmingPoolOverviewFabric

from overviews.fabrics.allocation.dexPoolAllocation.fabric import dexPoolAllocationOverviewFabric
from overviews.fabrics.allocation.lendingPoolAllocation.fabric import lendingPoolAllocationOverviewFabric
from overviews.fabrics.allocation.stakingPoolAllocation.fabric import stakingPoolAllocationOverviewFabric
from overviews.fabrics.allocation.farmingPoolAllocation.fabric import farmingPoolAllocationOverviewFabric

from overviews.fabrics.incentive.farmingPoolIncentive.fabric import farmingPoolIncentiveOverviewFabric
from overviews.fabrics.incentive.lendingPoolIncentive.fabric import lendingPoolIncentiveOverviewFabric
from overviews.fabrics.incentive.stakingPoolIncentive.fabric import stakingPoolIncentiveOverviewFabric


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

overviewAbstractFabric.addFabric(fabricType='lending-pool-borrow-overview', fabric=lendingPoolBorrowOverviewFabric)

overviewAbstractFabric.addFabric(fabricType='dex-pool-overview', fabric=dexPoolOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='lending-pool-overview', fabric=lendingPoolOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='staking-pool-overview', fabric=stakingPoolOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='farming-pool-overview', fabric=farmingPoolOverviewFabric)

overviewAbstractFabric.addFabric(fabricType='dex-pool-allocation-overview', fabric=dexPoolAllocationOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='lending-pool-allocation-overview', fabric=lendingPoolAllocationOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='staking-pool-allocation-overview', fabric=stakingPoolAllocationOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='farming-pool-allocation-overview', fabric=farmingPoolAllocationOverviewFabric)

overviewAbstractFabric.addFabric(fabricType='farming-pool-incentive-overview', fabric=farmingPoolIncentiveOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='lending-pool-incentive-overview', fabric=lendingPoolIncentiveOverviewFabric)
overviewAbstractFabric.addFabric(fabricType='staking-pool-incentive-overview', fabric=stakingPoolIncentiveOverviewFabric)
