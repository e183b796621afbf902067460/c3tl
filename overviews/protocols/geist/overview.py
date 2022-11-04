from overviews.protocols.aave.overview import (
    AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview, AaveV2LendingPoolBorrowOverview
)

from defi.protocols.geist.contracts.LendingPool import GeistLendingPoolContract


class GeistLendingPoolOverview(AaveV2LendingPoolOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolAllocationOverview(AaveV2LendingPoolAllocationOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolBorrowOverview(AaveV2LendingPoolBorrowOverview, GeistLendingPoolContract):
    pass
