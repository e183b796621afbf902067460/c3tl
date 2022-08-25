from head.interfaces.fabrics.interface import IConcreteFabric
from head.interfaces.overview.builder import IInstrumentOverview

from overviews.protocols.curve.overview import CurveLiquidityPoolOverview
from overviews.protocols.ellipsis.overview import EllipsisLiquidityPoolOverview
from overviews.protocols.uniswap.overview import UniswapV2LiquidityPoolOverview
from overviews.protocols.sushiswap.overview import SushiswapLiquidityPoolOverview
from overviews.protocols.pancakeswap.overview import PancakeSwapLiquidityPoolOverview


class LiquidityPoolOverviewFabric(IConcreteFabric):

    def addProduct(self, protocol: str, overview) -> None:
        if not self._products.get(protocol):
            self._products[protocol]: IInstrumentOverview = overview

    def getProduct(self, protocol: str) -> IInstrumentOverview:
        overview: IInstrumentOverview = self._products.get(protocol)
        if not overview:
            raise ValueError(f'Set Liquidity Overview handler for {protocol}')
        return overview


liquidityPoolOverviewFabric = LiquidityPoolOverviewFabric()

liquidityPoolOverviewFabric.addProduct(protocol='curve', overview=CurveLiquidityPoolOverview)
liquidityPoolOverviewFabric.addProduct(protocol='ellipsis', overview=EllipsisLiquidityPoolOverview)
liquidityPoolOverviewFabric.addProduct(protocol='uniswap', overview=UniswapV2LiquidityPoolOverview)
liquidityPoolOverviewFabric.addProduct(protocol='sushiswap', overview=SushiswapLiquidityPoolOverview)
liquidityPoolOverviewFabric.addProduct(protocol='pancakeswap', overview=PancakeSwapLiquidityPoolOverview)
