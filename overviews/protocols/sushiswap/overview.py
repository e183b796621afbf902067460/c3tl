from web3 import Web3

from defi.protocols.sushiswap.contracts.UniswapV2Pair import SushiSwapUniSwapV2PairContract
from defi.protocols.sushiswap.contracts.MasterChefV2 import SushiSwapMasterChefV2Contract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from head.bridge.configurator import BridgeConfigurator
from head.decorators.threadmethod import threadmethod

from providers.abstracts.fabric import providerAbstractFabric

from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolOverview
from overviews.protocols.pancakeswap.overview import (
    PancakeSwapFarmingPoolOverview, PancakeSwapFarmingPoolAllocationOverview
)


class SushiSwapDEXPoolOverview(UniSwapV2DEXPoolOverview, SushiSwapUniSwapV2PairContract):
    pass


class SushiSwapFarmingPoolOverview(PancakeSwapFarmingPoolOverview, SushiSwapUniSwapV2PairContract):
    _chiefContract: SushiSwapMasterChefV2Contract = SushiSwapMasterChefV2Contract()

    _providers: dict = {
        'eth': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='eth')\
                .produceProduct()
        }
    }

    _chiefAddresses: dict = {
        _providers['eth']['provider']:
            {
                'chief': '0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d'
            }
    }


class SushiSwapFarmingPoolAllocationOverview(PancakeSwapFarmingPoolAllocationOverview, SushiSwapFarmingPoolOverview):
    pass


class SushiSwapFarmingPoolIncentiveOverview(SushiSwapFarmingPoolAllocationOverview):
    @threadmethod
    def getOverview(self, address, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)
        chief: SushiSwapMasterChefV2Contract = self._chiefContract \
            .setAddress(address=self._chiefAddresses[self.provider]['chief']) \
            .setProvider(provider=self.provider) \
            .create()

        for i in range(chief.poolLength()):
            lp: str = chief.lpToken(i=i)
            if lp.lower() == self.address.lower():
                pid: int = i
                break
        else:
            raise ValueError()

        cake: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=chief.SUSHI()) \
            .setProvider(provider=self.provider) \
            .create()

        sushiSymbol: str = cake.symbol()
        sushiDecimals: int = cake.decimals()
        sushiPrice: float = self.trader.getPrice(major=sushiSymbol, vs='USD')

        sushies: float = chief.pendingSushi(_pid=pid, _user=address) / 10 ** sushiDecimals

        incentiveOverview: dict = {
            'pit_token_symbol': sushiSymbol,
            'pit_token_qty': sushies,
            'pit_token_price': sushiPrice
        }

        overview.append(incentiveOverview)
        return overview
