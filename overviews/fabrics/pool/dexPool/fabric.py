from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveDEXPoolOverview
from overviews.protocols.ellipsis.overview import EllipsisDEXPoolOverview
from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolOverview
from overviews.protocols.sushiswap.overview import SushiSwapDEXPoolOverview
from overviews.protocols.pancakeswap.overview import PancakeSwapDEXPoolOverview


class DEXPoolOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set DEX Overview handler for {protocol}')
        return overview


dexPoolOverviewFabric = DEXPoolOverviewFabric()

dexPoolOverviewFabric.addProduct(protocol='curve', overview=CurveDEXPoolOverview)
dexPoolOverviewFabric.addProduct(protocol='ellipsis', overview=EllipsisDEXPoolOverview)
dexPoolOverviewFabric.addProduct(protocol='uniswap', overview=UniSwapV2DEXPoolOverview)
dexPoolOverviewFabric.addProduct(protocol='sushiswap', overview=SushiSwapDEXPoolOverview)
dexPoolOverviewFabric.addProduct(protocol='pancakeswap', overview=PancakeSwapDEXPoolOverview)
