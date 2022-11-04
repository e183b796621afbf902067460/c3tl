from web3.exceptions import BadFunctionCallOutput

from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from overviews.protocols.aave.overview import AaveV2LendingPoolOverview

from defi.protocols.nereus.contracts.LendingPool import NereusLendingPoolContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class NereusLendingPoolOverview(AaveV2LendingPoolOverview, NereusLendingPoolContract):
    pass


class NereusLendingPoolAllocationOverview(IInstrumentOverview, NereusLendingPoolContract):
    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()

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
    @threadmethod
    def getOverview(self, address: str, *args, **kwargs):
        overview: list = list()

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
                        'healthFactor': healthFactor / 10 ** reserveToken.decimals()
                    }
                    overview.append(aOverview)
        return overview
