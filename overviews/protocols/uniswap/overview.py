from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.uniswap.contracts.UniswapV2Pair import UniswapV2PairContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class UniswapV2LiquidityPoolOverview(IInstrumentOverview, UniswapV2PairContract):

    @threadmethod
    def getOverview(self, *args, **kwargs) -> list:
        overview: list = list()

        t0Address: str = self.token0()
        t1Address: str = self.token1()

        t0: ERC20TokenContract = ERC20TokenContract()\
            .setAddress(address=t0Address)\
            .setProvider(provider=self.provider)\
            .create()
        t1: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=t1Address) \
            .setProvider(provider=self.provider) \
            .create()

        t0Symbol: str = t0.symbol()
        t1Symbol: str = t1.symbol()

        t0Decimals: int = t0.decimals()
        t1Decimals: int = t1.decimals()

        reserves: list = self.getReserves()
        t0Reserve: float = reserves[0] / 10 ** t0Decimals
        t1Reserve: float = reserves[1] / 10 ** t1Decimals

        t0Price: float = self.trader.getPrice(major=t0Symbol, vs='USD')
        t1Price: float = self.trader.getPrice(major=t1Symbol, vs='USD')

        t0Overview: dict = {
            'symbol': t0Symbol,
            'reserve': t0Reserve,
            'price': t0Price
        }
        t1Overview: dict = {
            'symbol': t1Symbol,
            'reserve': t1Reserve,
            'price': t1Price
        }

        overview.append(t0Overview)
        overview.append(t1Overview)

        return overview
