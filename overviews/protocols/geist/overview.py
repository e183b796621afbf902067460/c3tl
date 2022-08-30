from overviews.protocols.aave.overview import AaveV2LendingPoolOverview

from defi.protocols.geist.contracts.LendingPool import GeistLendingPoolContract


class GeistLendingPoolOverview(AaveV2LendingPoolOverview, GeistLendingPoolContract):
    pass
