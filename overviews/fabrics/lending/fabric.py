from overviews.fabrics.dex.fabric import DEXOverviewFabric

from overviews.protocols.aave.overview import AaveV2LendingPoolOverview


class LendingOverviewFabric(DEXOverviewFabric):
    pass


lendingOverviewFabric = LendingOverviewFabric()

lendingOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolOverview())
