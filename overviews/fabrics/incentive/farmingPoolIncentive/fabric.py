from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveFarmingPoolIncentiveOverview


class FarmingPoolIncentiveOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Farming Incentive Overview handler for {protocol}')
        return overview


farmingPoolIncentiveOverviewFabric = FarmingPoolIncentiveOverviewFabric()

farmingPoolIncentiveOverviewFabric.addProduct(protocol='curve', overview=CurveFarmingPoolIncentiveOverview)
