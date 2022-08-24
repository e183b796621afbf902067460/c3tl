from web3.exceptions import ContractLogicError

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.curve.contracts.Pool import CurvePoolContract
from defi.protocols.curve.contracts.Gauge import CurveGaugeContract
from defi.protocols.curve.tokens.LPToken import CurveLPTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class CurveLiquidityPoolOverview(IInstrumentOverview, CurvePoolContract):

    @threadmethod
    def getOverview(self, *args, **kwargs) -> list:
        overview: list = list()

        i: int = 0
        while True:
            try:
                tAddress: str = self.coins(arg0=i)
            except ContractLogicError:
                break

            t: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=tAddress)\
                .setProvider(provider=self.provider)\
                .create()

            decimals: int = t.decimals()
            symbol: str = t.symbol()
            reserve: float = self.balances(arg0=i) / 10 ** decimals
            price: float = self.trader.getPrice(major=symbol, vs='USD')

            aOverview: dict = {
                'symbol': symbol,
                'reserve': reserve,
                'price': price
            }
            overview.append(aOverview)
            i += 1

        return overview


class CurveStakingPoolOverview(IInstrumentOverview, CurveGaugeContract):

    @threadmethod
    def getOverview(self, *args, **kwargs) -> list:
        overview: list = list()

        tAddress: str = self.lp_token()
        t: CurveLPTokenContract = CurveLPTokenContract()\
                .setAddress(address=tAddress)\
                .setProvider(provider=self.provider)\
                .create()

        decimals: int = t.decimals()
        symbol: str = t.symbol()
        reserve: float = self.totalSupply() / 10 ** decimals
        price: float = self.trader.getPrice(major=symbol, vs='USD')

        aOverview: dict = {
            'symbol': symbol,
            'reserve': reserve,
            'price': price
        }
        overview.append(aOverview)

        return overview
