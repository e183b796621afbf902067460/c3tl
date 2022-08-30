from overviews.protocols.aave.overview import AaveV2LendingPoolOverview

from defi.protocols.sturdy.contracts.LendingPool import SturdyLendingPoolContract


class SturdyLendingPoolOverview(AaveV2LendingPoolOverview, SturdyLendingPoolContract):
    pass
