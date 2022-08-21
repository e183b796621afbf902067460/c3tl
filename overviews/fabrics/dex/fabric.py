from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveLiquidityPoolOverview
from overviews.protocols.ellipsis.overview import EllipsisLiquidityPoolOverview
from overviews.protocols.uniswap.overview import UniswapV2LiquidityPoolOverview
from overviews.protocols.sushiswap.overview import SushiswapLiquidityPoolOverview


class DEXOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set HTTP provider for {protocol} blockchain')
        return overview


dexOverviewFabric = DEXOverviewFabric()

dexOverviewFabric.addProduct(protocol='curve', overview=CurveLiquidityPoolOverview())
dexOverviewFabric.addProduct(protocol='ellipsis', overview=EllipsisLiquidityPoolOverview())
dexOverviewFabric.addProduct(protocol='uniswap', overview=UniswapV2LiquidityPoolOverview())
dexOverviewFabric.addProduct(protocol='sushiswap', overview=SushiswapLiquidityPoolOverview())
