from typing import TypeVar
from c3tl.interfaces.handlers.account_liquidations.interface import iAccountLiquidationsHandler


AccountLiquidationsHandler = TypeVar('AccountLiquidationsHandler', bound=iAccountLiquidationsHandler)
