from web3 import Web3

from defi.protocols.pancakeswap.contracts.PancakePair import PancakePairContract
from defi.protocols.pancakeswap.contracts.MasterChefV2 import PancakeSwapMasterChefV2Contract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod
from head.bridge.configurator import BridgeConfigurator

from providers.abstracts.fabric import providerAbstractFabric

from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolOverview


class PancakeSwapDEXPoolOverview(UniSwapV2DEXPoolOverview, PancakePairContract):
    pass


class PancakeSwapFarmingPoolOverview(IInstrumentOverview, PancakePairContract):
    _chiefContract: PancakeSwapMasterChefV2Contract = PancakeSwapMasterChefV2Contract()

    _providers: dict = {
        'bsc': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='bsc') \
                .produceProduct()
        }
    }

    _chiefAddresses: dict = {
        _providers['bsc']['provider']:
            {
                'chief': '0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652'
            }
    }

    @threadmethod
    def getOverview(self, *args, **kwargs) -> list:
        overview: list = list()

        t0Address: str = self.token0()
        t1Address: str = self.token1()

        t0: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=t0Address) \
            .setProvider(provider=self.provider) \
            .create()
        t1: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=t1Address) \
            .setProvider(provider=self.provider) \
            .create()

        t0Symbol: str = t0.symbol()
        t1Symbol: str = t1.symbol()

        t0Decimals: int = t0.decimals()
        t1Decimals: int = t1.decimals()

        totalSupply: int = self.totalSupply()
        totalLPLocked: int = self.balanceOf(address=self._chiefAddresses[self.provider]['chief'])

        share: float = totalLPLocked / totalSupply

        reserves: list = self.getReserves()
        t0Reserve: float = reserves[0] / 10 ** t0Decimals
        t1Reserve: float = reserves[1] / 10 ** t1Decimals

        t0Locked: float = share * t0Reserve
        t1Locked: float = share * t1Reserve

        t0Price: float = self.trader.getPrice(major=t0Symbol, vs='USD')
        t1Price: float = self.trader.getPrice(major=t1Symbol, vs='USD')

        t0Overview: dict = {
            'pit_token_symbol': t0Symbol,
            'pit_token_reserve': t0Locked,
            'pit_token_price': t0Price
        }

        t1Overview: dict = {
            'pit_token_symbol': t1Symbol,
            'pit_token_reserve': t1Locked,
            'pit_token_price': t1Price
        }

        overview.append(t0Overview)
        overview.append(t1Overview)
        return overview


class PancakeSwapFarmingPoolAllocationOverview(PancakeSwapFarmingPoolOverview):
    @threadmethod
    def getOverview(self, address, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)
        chief: PancakeSwapMasterChefV2Contract = self._chiefContract \
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

        farmingLP: int = chief.userInfo(pid=pid, address=address)[0]
        totalSupply: int = self.totalSupply()
        share: float = farmingLP / totalSupply

        t0Address: str = self.token0()
        t1Address: str = self.token1()

        t0: ERC20TokenContract = ERC20TokenContract() \
            .setAddress(address=t0Address) \
            .setProvider(provider=self.provider) \
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

        t0Amount: float = share * t0Reserve
        t1Amount: float = share * t1Reserve

        t0Price: float = self.trader.getPrice(major=t0Symbol, vs='USD')
        t1Price: float = self.trader.getPrice(major=t1Symbol, vs='USD')

        t0Overview: dict = {
            'pit_token_symbol': t0Symbol,
            'pit_token_amount': t0Amount,
            'pit_token_price': t0Price
        }

        t1Overview: dict = {
            'pit_token_symbol': t1Symbol,
            'pit_token_amount': t1Amount,
            'pit_token_price': t1Price
        }

        overview.append(t0Overview)
        overview.append(t1Overview)
        return overview


class PancakeSwapFarmingPoolIncentiveOverview(PancakeSwapFarmingPoolOverview):
    @threadmethod
    def getOverview(self, address, *args, **kwargs) -> list:
        overview: list = list()

        address: str = Web3.toChecksumAddress(address)
        chief: PancakeSwapMasterChefV2Contract = self._chiefContract \
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

        cake: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=chief.CAKE())\
                .setProvider(provider=self.provider)\
                .create()

        cakeSymbol: str = cake.symbol()
        cakeDecimals: int = cake.decimals()
        cakePrice: float = self.trader.getPrice(major=cakeSymbol, vs='USD')

        cakes: float = chief.pendingCake(_pid=pid, _user=address) / 10 ** cakeDecimals

        incentiveOverview: dict = {
            'pit_token_symbol': cakeSymbol,
            'pit_token_amount': cakes,
            'pit_token_price': cakePrice
        }

        overview.append(incentiveOverview)
        return overview
