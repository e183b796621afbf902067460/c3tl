from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

from overviews.protocols.aave.overview import (
    AaveV2LendingPoolOverview, AaveV2LendingPoolAllocationOverview, AaveV2LendingPoolBorrowOverview
)

from head.bridge.configurator import BridgeConfigurator
from head.decorators.threadmethod import threadmethod
from head.interfaces.overview.builder import IInstrumentOverview

from defi.protocols.geist.contracts.LendingPool import GeistLendingPoolContract
from defi.protocols.geist.contracts.ChefIncentivesController import GeistChiefIncentivesControllerContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from providers.abstracts.fabric import providerAbstractFabric


class GeistLendingPoolOverview(AaveV2LendingPoolOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolAllocationOverview(AaveV2LendingPoolAllocationOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolBorrowOverview(AaveV2LendingPoolBorrowOverview, GeistLendingPoolContract):
    pass


class GeistLendingPoolIncentiveOverview(IInstrumentOverview, GeistLendingPoolContract):
    _controllerContract: GeistChiefIncentivesControllerContract = GeistChiefIncentivesControllerContract()

    _providers: dict = {
        'ftm': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='ftm')\
                .produceProduct()
        }
    }

    _controllerAddresses: dict = {
        _providers['ftm']['provider']:
            {
                'controller': '0x297FddC5c33Ef988dd03bd13e162aE084ea1fE57'
            }
    }

    _geistAddresses: dict = {
        _providers['ftm']['provider']:
            {
                'geist': '0xd8321AA83Fb0a4ECd6348D4577431310A6E0814d'
            }
    }

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0])[2:]
        reservesList: list = self.getReservesList()

        totalIncentives: int = 0
        for i, mask in enumerate(userConfiguration[::-1]):
            if mask == '1' and i % 2:
                reserveTokenAddress: str = reservesList[i // 2]
                try:
                    reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
                except BadFunctionCallOutput:
                    continue

                incentivesController: GeistChiefIncentivesControllerContract = self._controllerContract \
                    .setAddress(self._controllerAddresses[self.provider]['controller']) \
                    .setProvider(provider=self.provider) \
                    .create()

                gTokenAddress: str = reserveData[7]
                incentivesAmount: list = incentivesController.claimableReward(tokens=[gTokenAddress], address=address)[0]
                totalIncentives += incentivesAmount

        if totalIncentives:
            geist: ERC20TokenContract = ERC20TokenContract()\
                    .setAddress(address=self._geistAddresses[self.provider]['geist'])\
                    .setProvider(provider=self.provider)\
                    .create()
            geistSymbol: str = geist.symbol()
            geistDecimals: int = geist.decimals()
            geistPrice: float = self.trader.getPrice(major=geistSymbol, vs='USD')

            aOverview: dict = {
                'symbol': geistSymbol,
                'amount': totalIncentives / 10 ** geistDecimals,
                'price': geistPrice
            }
            overview.append(aOverview)
        return overview
