from web3.exceptions import ContractLogicError
from web3 import Web3

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.curve.contracts.Pool import CurvePoolContract
from defi.protocols.curve.contracts.Gauge import CurveGaugeContract
from defi.protocols.curve.contracts.LiquidityGauge import CurveLiquidityGauge
from defi.protocols.curve.tokens.LPToken import CurveLPTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class CurveDEXPoolOverview(IInstrumentOverview, CurvePoolContract):

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
                'pit_token_symbol': symbol,
                'pit_token_reserve': reserve,
                'pit_token_price': price
            }
            overview.append(aOverview)
            i += 1

        return overview


class CurveFarmingPoolOverview(IInstrumentOverview, CurveGaugeContract):

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
            'pit_token_symbol': symbol,
            'pit_token_reserve': reserve,
            'pit_token_price': price
        }
        overview.append(aOverview)

        return overview


class CurveFarmingPoolAllocationOverview(IInstrumentOverview, CurveGaugeContract):

    @threadmethod
    def getOverview(self, address, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)

        tAddress: str = self.lp_token()
        t: CurveLPTokenContract = CurveLPTokenContract() \
            .setAddress(address=tAddress) \
            .setProvider(provider=self.provider) \
            .create()
        symbol: str = t.symbol()
        decimals: int = t.decimals()
        price: float = self.trader.getPrice(major=symbol, vs='USD')

        balanceOf: int = self.balanceOf(address=address)

        allocationOverview: dict = {
            'pit_token_symbol': symbol,
            'pit_token_amount': balanceOf / 10 ** decimals,
            'pit_token_price': price
        }
        overview.append(allocationOverview)
        return overview


class CurveFarmingPoolIncentiveOverview(IInstrumentOverview, CurveLiquidityGauge):

    @threadmethod
    def getOverview(self, address, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)

        gaugeDecimals: int = self.decimals()

        crvAddress: str = self.crv_token()
        crv: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=crvAddress) \
            .setProvider(provider=self.provider) \
            .create()
        crvSymbol: str = crv.symbol()
        crvDecimals: int = crv.decimals()
        crvPrice: float = self.trader.getPrice(major=crvSymbol, vs='USD')

        crvIncentives: int = self.claimable_tokens(address=address)

        crvOverview: dict = {
            'pit_token_symbol': crvSymbol,
            'pit_token_amount': crvIncentives / 10 ** crvDecimals,
            'pit_token_price': crvPrice
        }
        overview.append(crvOverview)

        i: int = 0
        while True:
            try:
                tAddress: str = self.reward_tokens(i=i)
                if tAddress == '0x0000000000000000000000000000000000000000':
                    break
            except ContractLogicError:
                break


            t: ERC20TokenContract = ERC20TokenContract() \
                .setAddress(address=tAddress) \
                .setProvider(provider=self.provider) \
                .create()

            decimals: int = t.decimals()
            symbol: str = t.symbol()
            price: float = self.trader.getPrice(major=symbol, vs='USD')

            rewardIntegral: int = self.reward_integral(address=tAddress)
            rewardIntegralFor: int = self.reward_integral_for(token=tAddress, address=address)

            incentives: float = self.balanceOf(address=address) / 10 ** gaugeDecimals * (rewardIntegral - rewardIntegralFor) / 10 ** gaugeDecimals if rewardIntegralFor < rewardIntegral else 0

            tOverview: dict = {
                'pit_token_symbol': symbol,
                'pit_token_amount': incentives / 10 ** decimals,
                'pit_token_price': price
            }
            overview.append(tOverview)
            i += 1

        return overview
