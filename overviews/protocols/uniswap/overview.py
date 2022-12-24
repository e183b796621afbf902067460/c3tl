from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.uniswap.contracts.UniswapV2Pair import UniSwapV2PairContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class UniSwapV2DEXPoolOverview(IInstrumentOverview, UniSwapV2PairContract):

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
            'pit_token_symbol': t0Symbol,
            'pit_token_qty': t0Reserve,
            'pit_token_price': t0Price
        }
        t1Overview: dict = {
            'pit_token_symbol': t1Symbol,
            'pit_token_qty': t1Reserve,
            'pit_token_price': t1Price
        }

        overview.append(t0Overview)
        overview.append(t1Overview)

        return overview


class UniSwapV2DEXPoolAllocationOverview(IInstrumentOverview, UniSwapV2PairContract):

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs) -> list:
        overview: list = list()

        amount: int = self.balanceOf(address=address)
        totalSupply: int = self.totalSupply()

        share: float = amount / totalSupply

        t0Address: str = self.token0()
        t1Address: str = self.token1()

        t0: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=t0Address)\
                .setProvider(provider=self.provider)\
                .create()
        t1: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=t1Address)\
                .setProvider(provider=self.provider)\
                .create()

        t0Symbol: str = t0.symbol()
        t1Symbol: str = t1.symbol()

        t0Decimals: int = t0.decimals()
        t1Decimals: int = t1.decimals()

        reserves: list = self.getReserves()
        t0Reserve: float = reserves[0] / 10 ** t0Decimals
        t1Reserve: float = reserves[1] / 10 ** t1Decimals

        t0Amount: float = share * t0Reserve
        t1Amount: float = share * t1Reserve

        t0Price: float = self.trader.getPrice(major=t0Symbol, vs='USD')
        t1Price: float = self.trader.getPrice(major=t1Symbol, vs='USD')

        t0Overview: dict = {
            'pit_token_symbol': t0Symbol,
            'pit_token_qty': t0Amount,
            'pit_token_price': t0Price
        }

        t1Overview: dict = {
            'pit_token_symbol': t1Symbol,
            'pit_token_qty': t1Amount,
            'pit_token_price': t1Price
        }

        overview.append(t0Overview)
        overview.append(t1Overview)
        return overview

