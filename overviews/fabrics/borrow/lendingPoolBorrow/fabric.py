from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.aave.overview import AaveV2LendingPoolBorrowOverview
from overviews.protocols.geist.overview import GeistLendingPoolBorrowOverview
from overviews.protocols.nereus.overview import NereusLendingPoolBorrowOverview


class LendingPoolBorrowOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Lending Borrow Overview handler for {protocol}')
        return overview


lendingPoolBorrowOverviewFabric = LendingPoolBorrowOverviewFabric()

lendingPoolBorrowOverviewFabric.addProduct(protocol='aave', overview=AaveV2LendingPoolBorrowOverview)
lendingPoolBorrowOverviewFabric.addProduct(protocol='geist', overview=GeistLendingPoolBorrowOverview)
lendingPoolBorrowOverviewFabric.addProduct(protocol='nereus', overview=NereusLendingPoolBorrowOverview)
