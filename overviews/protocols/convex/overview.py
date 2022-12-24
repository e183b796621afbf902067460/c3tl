from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod
from head.bridge.configurator import BridgeConfigurator

from defi.protocols.convex.contracts.BaseRewardPool import ConvexBaseRewardPoolContract
from defi.protocols.convex.tokens.DepositToken import ConvexDepositTokenContract
from defi.protocols.convex.tokens.ConvexToken import ConvexTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from providers.abstracts.fabric import providerAbstractFabric

from web3 import Web3


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
            'pit_token_symbol': symbol,
            'pit_token_qty': reserve,
            'pit_token_price': price
        }
        overview.append(aOverview)

        return overview


class ConvexStakingPoolAllocationOverview(IInstrumentOverview, ConvexBaseRewardPoolContract):

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)

        tAddress: str = self.stakingToken()
        t: ConvexDepositTokenContract = ConvexDepositTokenContract()\
                .setAddress(address=tAddress)\
                .setProvider(provider=self.provider)\
                .create()
        symbol: str = t.symbol()
        decimals: int = t.decimals()
        price: float = self.trader.getPrice(major=symbol, vs='USD')

        balanceOf: int = self.balanceOf(address=address)

        allocationOverview: dict = {
            'pit_token_symbol': symbol,
            'pit_token_qty': balanceOf / 10 ** decimals,
            'pit_token_price': price
        }
        overview.append(allocationOverview)
        return overview


class ConvexStakingPoolIncentiveOverview(IInstrumentOverview, ConvexBaseRewardPoolContract):
    _rewardContract: ConvexBaseRewardPoolContract = ConvexBaseRewardPoolContract()

    _providers: dict = {
        'eth': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='eth') \
                .produceProduct()
        }
    }

    _convexAddresses: dict = {
        _providers['eth']['provider']:
            {
                'convex': '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B'
            }
    }

    def _getCvxIncentiveOverview(self, crv: float) -> dict:
        cvx: ConvexTokenContract = ConvexTokenContract() \
            .setAddress(address=self._convexAddresses[self.provider]['convex']) \
            .setProvider(provider=self.provider) \
            .create()
        cvxSymbol: str = cvx.symbol()
        cvxDecimals: int = cvx.decimals()
        cvxPrice: float = self.trader.getPrice(major=cvxSymbol, vs='USD')

        cvxMaxSupply: int = cvx.maxSupply() / 10 ** cvxDecimals
        cvxTotalCliffs: int = cvx.totalCliffs()
        cvxCliffSize: int = cvxMaxSupply // cvxTotalCliffs

        cvxTotalSupply: int = cvx.totalSupply() / 10 ** cvxDecimals
        currentCliff: float = cvxTotalSupply / cvxCliffSize

        if currentCliff < cvxTotalCliffs:
            remain: float = cvxTotalCliffs - currentCliff
            cvx: float = crv * remain / cvxTotalCliffs
            amount: float = cvxMaxSupply - cvxTotalSupply\

            cvxOverview: dict = {
                'pit_token_symbol': cvxSymbol,
                'pit_token_qty': min(cvx, amount),
                'pit_token_price': cvxPrice
            }
            return cvxOverview
        return dict()

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)

        crvAddress: str = self.rewardToken()
        extra: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=crvAddress)\
                .setProvider(provider=self.provider)\
                .create()
        crvSymbol: str = extra.symbol()
        crvDecimals: int = extra.decimals()
        crvPrice: float = self.trader.getPrice(major=crvSymbol, vs='USD')

        balanceOf: int = self.earned(address=address) / 10 ** crvDecimals

        crvOverview: dict = {
            'pit_token_symbol': crvSymbol,
            'pit_token_qty': balanceOf,
            'pit_token_price': crvPrice
        }
        overview.append(crvOverview)

        cvxIncentiveOverview: dict = self._getCvxIncentiveOverview(crv=balanceOf)
        if cvxIncentiveOverview:
            overview.append(cvxIncentiveOverview)

        for i in range(self.extraRewardsLength()):
            gauge: ConvexBaseRewardPoolContract = ConvexBaseRewardPoolContract()\
                    .setAddress(address=self.extraRewards(i=i))\
                    .setProvider(provider=self.provider)\
                    .create()

            extraAddress: str = gauge.rewardToken()
            extra: ERC20TokenContract = ERC20TokenContract() \
                .setAddress(address=extraAddress) \
                .setProvider(provider=self.provider) \
                .create()
            extraSymbol: str = extra.symbol()
            extraDecimals: int = extra.decimals()
            extraPrice: float = self.trader.getPrice(major=extraSymbol, vs='USD')

            balanceOf: int = gauge.earned(address=address) / 10 ** extraDecimals

            extraOverview: dict = {
                'pit_token_symbol': extraSymbol,
                'pit_token_qty': balanceOf,
                'pit_token_price': extraPrice
            }
            overview.append(extraOverview)
        return overview
