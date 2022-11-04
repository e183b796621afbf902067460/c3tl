from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolAllocationOverview


class DEXPoolAllocationOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set DEX Allocation Overview handler for {protocol}')
        return overview


dexPoolAllocationOverviewFabric = DEXPoolAllocationOverviewFabric()

dexPoolAllocationOverviewFabric.addProduct(protocol='uniswap', overview=UniSwapV2DEXPoolAllocationOverview)
