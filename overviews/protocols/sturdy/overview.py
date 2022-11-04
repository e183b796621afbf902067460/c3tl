from overviews.protocols.aave.overview import AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview

from defi.protocols.sturdy.contracts.LendingPool import SturdyLendingPoolContract


class SturdyLendingPoolOverview(AaveV2LendingPoolOverview, SturdyLendingPoolContract):
    pass


class SturdyLendingPoolAllocationOverview(AaveV2LendingPoolAllocationOverview, SturdyLendingPoolContract):
    pass
