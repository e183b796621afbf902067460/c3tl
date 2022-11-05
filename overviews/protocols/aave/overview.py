from web3.exceptions import BadFunctionCallOutput
from web3 import Web3

from head.bridge.configurator import BridgeConfigurator
from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.aave.contracts.LendingPool import AaveLendingPoolV2Contract
from defi.protocols.aave.contracts.IncentivesController import AaveIncentivesControllerV2Contract
from defi.protocols.aave.tokens.AToken import ATokenContract
from defi.protocols.aave.tokens.VariableDebtToken import VariableDebtTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract

from providers.abstracts.fabric import providerAbstractFabric


class AaveV2LendingPoolOverview(IInstrumentOverview, AaveLendingPoolV2Contract):
    _RAY: int = 10 ** 27
    _SECONDS_PER_YEAR: int = 31536000

    @threadmethod
    def getOverview(self, *args, **kwargs):
        overview: list = list()

        reservesList: list = self.getReservesList()
        for reserveAddress in reservesList:
            try:
                reserveData: tuple = self.getReserveData(asset=reserveAddress)
            except BadFunctionCallOutput:
                continue

            liquidityRate, variableBorrowRate = reserveData[3], reserveData[4]
            depositAPR, variableBorrowAPR = liquidityRate / self._RAY, variableBorrowRate / self._RAY

            depositAPY = ((1 + (depositAPR / self._SECONDS_PER_YEAR)) ** self._SECONDS_PER_YEAR) - 1
            variableBorrowAPY = ((1 + (variableBorrowAPR / self._SECONDS_PER_YEAR)) ** self._SECONDS_PER_YEAR) - 1

            aTokenAddress, variableDebtTokenAddress = reserveData[7], reserveData[9]

            aToken: ATokenContract = ATokenContract()\
                .setAddress(address=aTokenAddress)\
                .setProvider(provider=self.provider)\
                .create()
            variableDebtToken: VariableDebtTokenContract = VariableDebtTokenContract()\
                .setAddress(address=variableDebtTokenAddress)\
                .setProvider(provider=self.provider)\
                .create()
            t: ERC20TokenContract = ERC20TokenContract()\
                .setAddress(address=reserveAddress)\
                .setProvider(provider=self.provider)\
                .create()

            try:
                tSymbol: str = t.symbol()
            except OverflowError:
                continue

            aTokenDecimals: int = aToken.decimals()
            variableDebtTokenDecimals: int = variableDebtToken.decimals()

            totalReserveSize: float = aToken.totalSupply() / 10 ** aTokenDecimals
            totalBorrowSize: float = variableDebtToken.totalSupply() / 10 ** variableDebtTokenDecimals

            tPrice: float = self.trader.getPrice(major=tSymbol, vs='USD')

            aOverview: dict = {
                'symbol': tSymbol,
                'reserve': totalReserveSize,
                'borrow': totalBorrowSize,
                'price': tPrice,
                'depositAPY': depositAPY * 100,
                'borrowAPY': variableBorrowAPY * 100
            }
            overview.append(aOverview)
        return overview


class AaveV2LendingPoolAllocationOverview(IInstrumentOverview, AaveLendingPoolV2Contract):

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0])[2:]
        reservesList: list = self.getReservesList()
        for i, mask in enumerate(userConfiguration[::-1]):
            reserveTokenAddress: str = reservesList[i // 2]
            try:
                reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
            except BadFunctionCallOutput:
                continue
            if mask == '1':
                if i % 2:
                    reserveToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=reserveTokenAddress)\
                                .setProvider(provider=self.provider)\
                                .create()
                    try:
                        reserveTokenSymbol: str = reserveToken.symbol()
                    except OverflowError:
                        continue
                    reserveTokenPrice: float = self.trader.getPrice(major=reserveTokenSymbol, vs='USD')

                    aTokenAddress: str = reserveData[7]
                    aToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=aTokenAddress)\
                                .setProvider(provider=self.provider)\
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


class AaveV2LendingPoolBorrowOverview(IInstrumentOverview, AaveLendingPoolV2Contract):
    _DECIMALS: int = 18

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0])[2:]
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
                    reserveToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=reserveTokenAddress)\
                                .setProvider(provider=self.provider)\
                                .create()
                    try:
                        reserveTokenSymbol: str = reserveToken.symbol()
                    except OverflowError:
                        continue
                    reserveTokenPrice: float = self.trader.getPrice(major=reserveTokenSymbol, vs='USD')

                    stableDebtTokenAddress: str = reserveData[8]
                    variableDebtTokenAddress: str = reserveData[9]

                    stableDebtToken: ERC20TokenContract = ERC20TokenContract()\
                                .setAddress(address=stableDebtTokenAddress)\
                                .setProvider(provider=self.provider)\
                                .create()
                    variableDebtToken: ERC20TokenContract = ERC20TokenContract()\
                        .setAddress(address=variableDebtTokenAddress)\
                        .setProvider(provider=self.provider)\
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


class AaveV2LendingPoolIncentiveOverview(IInstrumentOverview, AaveLendingPoolV2Contract):
    _controllerContract: AaveIncentivesControllerV2Contract = AaveIncentivesControllerV2Contract()

    _providers: dict = {
        'eth': {
            'provider': BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey='eth') \
                .produceProduct()
        }
    }

    _controllerAddresses: dict = {
        _providers['eth']['provider']:
            {
                'controller': '0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5'
            }
    }

    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()
        address: str = Web3.toChecksumAddress(value=address)

        userConfiguration: str = bin(self.getUserConfiguration(address=address)[0])[2:]
        reservesList: list = self.getReservesList()
        for i, mask in enumerate(userConfiguration[::-1]):
            if mask == '1' and i % 2:
                reserveTokenAddress: str = reservesList[i // 2]
                try:
                    reserveData: tuple = self.getReserveData(asset=reserveTokenAddress)
                except BadFunctionCallOutput:
                    continue

                incentivesController: AaveIncentivesControllerV2Contract = self._controllerContract \
                    .setAddress(self._controllerAddresses[self.provider]['controller']) \
                    .setProvider(provider=self.provider) \
                    .create()

                aTokenAddress: str = reserveData[7]

                incentivesAmount: int = incentivesController.getRewardsBalance(assets=[aTokenAddress], address=address)
                if incentivesAmount:
                    rewardTokenAddress: str = incentivesController.REWARD_TOKEN()
                    rewardToken: ERC20TokenContract = ERC20TokenContract()\
                            .setAddress(address=rewardTokenAddress)\
                            .setProvider(provider=self.provider)\
                            .create()
                    rewardDecimals: int = rewardToken.decimals()
                    rewardSymbol: str = rewardToken.symbol()
                    rewardPrice: float = self.trader.getPrice(major=rewardSymbol, vs='USD')

                    aOverview: dict = {
                        'symbol': rewardSymbol,
                        'amount': incentivesAmount / 10 ** rewardDecimals,
                        'price': rewardPrice
                    }
                    if aOverview not in overview:
                        overview.append(aOverview)
        return overview

