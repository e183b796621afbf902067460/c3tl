from overviews.protocols.aave.overview import AaveV2LendingPoolOverview

from defi.protocols.nereus.contracts.LendingPool import NereusLendingPoolContract


class NereusLendingPoolOverview(AaveV2LendingPoolOverview, NereusLendingPoolContract):
    pass
