from defi.protocols.sushiswap.contracts.UniswapV2Pair import SushiSwapUniSwapV2PairContract
from defi.protocols.sushiswap.contracts.MasterChefV2 import SushiSwapMasterChefV2Contract

from head.bridge.configurator import BridgeConfigurator

from providers.abstracts.fabric import providerAbstractFabric

from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolOverview
from overviews.protocols.pancakeswap.overview import PancakeSwapFarmingPoolAllocationOverview


class SushiSwapDEXPoolOverview(UniSwapV2DEXPoolOverview, SushiSwapUniSwapV2PairContract):
    pass


class SushiSwapFarmingPoolAllocationOverview(PancakeSwapFarmingPoolAllocationOverview, SushiSwapUniSwapV2PairContract):
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
