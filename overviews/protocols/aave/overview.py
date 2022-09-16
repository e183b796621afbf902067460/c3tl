from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.aave.contracts.LendingPool import AaveLendingPoolV2Contract
from defi.protocols.aave.tokens.AToken import ATokenContract
from defi.protocols.aave.tokens.VariableDebtToken import VariableDebtTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class AaveV2LendingPoolOverview(IInstrumentOverview, AaveLendingPoolV2Contract):
    _RAY: int = 10 ** 27
    _SECONDS_PER_YEAR = 31536000

    @threadmethod
    def getOverview(self, *args, **kwargs):
        overview: list = list()

        reservesList: list = self.getReservesList()
        for reserveAddress in reservesList:
            if self.trader.isStablecoin(address=reserveAddress):
                reserveData: tuple = self.getReserveData(asset=reserveAddress)

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

                tSymbol: str = t.symbol()

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
                    'depositAPY': depositAPY,
                    'borrowAPY': variableBorrowAPY
                }
                overview.append(aOverview)
        return overview
