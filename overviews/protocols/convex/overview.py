from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.convex.contracts.BaseRewardPool import ConvexBaseRewardPoolContract
from defi.protocols.convex.tokens.DepositToken import ConvexDepositTokenContract


class ConvexStakingPoolOverview(IInstrumentOverview, ConvexBaseRewardPoolContract):

    @threadmethod
    def getOverview(self, *args, **kwargs) -> list:
        overview: list = list()

        tAddress: str = self.stakingToken()
        t: ConvexDepositTokenContract = ConvexDepositTokenContract()\
            .setAddress(address=tAddress)\
            .setProvider(provider=self.provider)\
            .create()

        symbol: str = t.symbol()
        decimals: int = t.decimals()
        reserve: float = self.totalSupply() / 10 ** decimals
        price: float = self.trader.getPrice(major=symbol, vs='USD')

        aOverview: dict = {
            'symbol': symbol,
            'reserve': reserve,
            'price': price
        }
        overview.append(aOverview)

        return overview
