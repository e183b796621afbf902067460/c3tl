from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.aave.overview import AaveV2LendingPoolAllocationOverview
from overviews.protocols.geist.overview import GeistLendingPoolAllocationOverview
from overviews.protocols.nereus.overview import NereusLendingPoolAllocationOverview


class LendingPoolAllocationOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Lending Allocation Overview handler for {protocol}')
        return overview


lendingPoolAllocationOverviewFabric = LendingPoolAllocationOverviewFabric()

lendingPoolAllocationOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolAllocationOverview)
lendingPoolAllocationOverviewFabric.addProduct(protocol='geist', overview=GeistLendingPoolAllocationOverview)
lendingPoolAllocationOverviewFabric.addProduct(protocol='nereus', overview=NereusLendingPoolAllocationOverview)
