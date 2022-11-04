from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveFarmingPoolAllocationOverview
from overviews.protocols.ellipsis.overview import EllipsisFarmingPoolAllocationOverview
from overviews.protocols.pancakeswap.overview import PancakeSwapFarmingPoolAllocationOverview


class FarmingPoolAllocationOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Farming Allocation Overview handler for {protocol}')
        return overview


farmingPoolAllocationOverviewFabric = FarmingPoolAllocationOverviewFabric()

farmingPoolAllocationOverviewFabric.addProduct(protocol='curve', overview=CurveFarmingPoolAllocationOverview)
farmingPoolAllocationOverviewFabric.addProduct(protocol='ellipsis', overview=EllipsisFarmingPoolAllocationOverview)
farmingPoolAllocationOverviewFabric.addProduct(protocol='pancakeswap', overview=PancakeSwapFarmingPoolAllocationOverview)
