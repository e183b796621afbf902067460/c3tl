from head.interfaces.overview.builder import IInstrumentOverview
from head.decorators.threadmethod import threadmethod

from defi.protocols.aave.contracts.LendingPool import AaveLendingPoolV2Contract
from defi.protocols.aave.tokens.AToken import ATokenContract
from defi.protocols.aave.tokens.VariableDebtToken import VariableDebtTokenContract
from defi.tokens.contracts.ERC20Token import ERC20TokenContract


class AaveV2LendingPoolOverview(IInstrumentOverview, AaveLendingPoolV2Contract):

    @threadmethod
    def getOverview(self, asset: str, *args, **kwargs):
        overview: list = list()

        reserveData: list = self.getReserveData(asset=asset)

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
            .setAddress(address=asset)\
            .setProvider(provider=self.provider)\
            .create()

        tSymbol: str = t.symbol()

        aTokenDecimals: int = aToken.decimals()
        variableDebtTokenDecimals: int = variableDebtToken.decimals()

        totalReserveSize: float = aToken.totalSupply() / 10 ** aTokenDecimals
        totalBorrowSize: float = variableDebtToken.totalSupply() / 10 ** variableDebtTokenDecimals

        tPrice: float = self.trader.getPrice(major=tSymbol, vs='USD')

        aOverview: dict = {
            'reserve': totalReserveSize,
            'borrow': totalBorrowSize,
            'price': tPrice
        }
        overview.append(aOverview)
        return overview
