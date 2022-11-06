from web3.exceptions import BadFunctionCallOutput
from web3 import Web3

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod
from head.bridge.configurator import BridgeConfigurator

from overviews.protocols.aave.overview import AaveV2LendingPoolOverview

from defi.protocols.nereus.contracts.LendingPool import NereusLendingPoolContract
from defi.protocols.nereus.contracts.ChefIncentivesController import NereusChiefIncentivesControllerContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from providers.abstracts.fabric import providerAbstractFabric


class NereusLendingPoolOverview(AaveV2LendingPoolOverview, NereusLendingPoolContract):
    pass


class NereusLendingPoolAllocationOverview(IInstrumentOverview, NereusLendingPoolContract):
    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0][0])[2:]
        reservesList: list = self.getReservesList()
        for i, mask in enumerate(userConfiguration[::-1]):
            reserveTokenAddress: str = reservesList[i // 2]
            try:
                reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
            except BadFunctionCallOutput:
                continue
            if mask == '1':
                if i % 2:
                    reserveToken: ERC20TokenContract = ERC20TokenContract() \
                        .setAddress(address=reserveTokenAddress) \
                        .setProvider(provider=self.provider) \
                        .create()
                    try:
                        reserveTokenSymbol: str = reserveToken.symbol()
                    except OverflowError:
                        continue
                    reserveTokenPrice: float = self.trader.getPrice(major=reserveTokenSymbol, vs='USD')

                    aTokenAddress: str = reserveData[7]
                    aToken: ERC20TokenContract = ERC20TokenContract() \
                        .setAddress(address=aTokenAddress) \
                        .setProvider(provider=self.provider) \
                        .create()
                    aTokenDecimals: int = aToken.decimals()
                    collateral: int = aToken.balanceOf(address=address) / 10 ** aTokenDecimals

                    aOverview: dict = {
                        'symbol': reserveTokenSymbol,
                        'amount': collateral,
                        'price': reserveTokenPrice
                    }
                    overview.append(aOverview)
        return overview


class NereusLendingPoolBorrowOverview(IInstrumentOverview, NereusLendingPoolContract):
    _DECIMALS: int = 18

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0][0])[2:]
        reservesList: list = self.getReservesList()

        accountData: list = self.getUserAccountData(address=address)
        healthFactor: int = accountData[5]

        for i, mask in enumerate(userConfiguration[::-1]):
            reserveTokenAddress: str = reservesList[i // 2]
            try:
                reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
            except BadFunctionCallOutput:
                continue
            if mask == '1':
                if not i % 2:
                    reserveToken: ERC20TokenContract = ERC20TokenContract() \
                        .setAddress(address=reserveTokenAddress) \
                        .setProvider(provider=self.provider) \
                        .create()
                    try:
                        reserveTokenSymbol: str = reserveToken.symbol()
                    except OverflowError:
                        continue
                    reserveTokenPrice: float = self.trader.getPrice(major=reserveTokenSymbol, vs='USD')

                    stableDebtTokenAddress: str = reserveData[8]
                    variableDebtTokenAddress: str = reserveData[9]

                    stableDebtToken: ERC20TokenContract = ERC20TokenContract() \
                        .setAddress(address=stableDebtTokenAddress) \
                        .setProvider(provider=self.provider) \
                        .create()
                    variableDebtToken: ERC20TokenContract = ERC20TokenContract() \
                        .setAddress(address=variableDebtTokenAddress) \
                        .setProvider(provider=self.provider) \
                        .create()

                    stableDebtTokenDecimals: int = stableDebtToken.decimals()
                    variableDebtTokenDecimals: int = variableDebtToken.decimals()

                    debt: int = stableDebtToken.balanceOf(address=address) / 10 ** stableDebtTokenDecimals + \
                                variableDebtToken.balanceOf(address=address) / 10 ** variableDebtTokenDecimals

                    aOverview: dict = {
                        'symbol': reserveTokenSymbol,
                        'amount': debt,
                        'price': reserveTokenPrice,
                        'healthFactor': healthFactor / 10 ** self._DECIMALS
                    }
                    overview.append(aOverview)
        return overview


class NereusLendingPoolIncentiveOverview(IInstrumentOverview, NereusLendingPoolContract):
    _controllerContract: NereusChiefIncentivesControllerContract = NereusChiefIncentivesControllerContract()

    _providers: dict = {
        'avax': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='avax') \
                .produceProduct()
        }
    }

    _controllerAddresses: dict = {
        _providers['avax']['provider']:
            {
                'controller': '0xa57a8C5dd29bd9CC605027E62935db2cB5485378'
            }
    }
    _nereusAddresses: dict = {
        _providers['avax']['provider']:
            {
                'wirex': '0xfcDe4A87b8b6FA58326BB462882f1778158B02F1'
            }
    }

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0][0])[2:]
        reservesList: list = self.getReservesList()

        totalIncentives: int = 0
        for i, mask in enumerate(userConfiguration[::-1]):
            if mask == '1' and i % 2:
                reserveTokenAddress: str = reservesList[i // 2]
                try:
                    reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
                except BadFunctionCallOutput:
                    continue

                incentivesController: NereusChiefIncentivesControllerContract = self._controllerContract \
                    .setAddress(self._controllerAddresses[self.provider]['controller']) \
                    .setProvider(provider=self.provider) \
                    .create()

                gTokenAddress: str = reserveData[7]
                incentivesAmount: list = incentivesController.claimableReward(tokens=[gTokenAddress], address=address)[
                    0]
                totalIncentives += incentivesAmount

        if totalIncentives:
            geist: ERC20TokenContract = ERC20TokenContract() \
                .setAddress(address=self._nereusAddresses[self.provider]['wirex']) \
                .setProvider(provider=self.provider) \
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
