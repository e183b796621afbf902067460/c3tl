from overviews.protocols.aave.overview import AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview

from defi.protocols.geist.contracts.LendingPool import GeistLendingPoolContract


class GeistLendingPoolOverview(AaveV2LendingPoolOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolAllocationOverview(AaveV2LendingPoolAllocationOverview, GeistLendingPoolContract):
    pass
