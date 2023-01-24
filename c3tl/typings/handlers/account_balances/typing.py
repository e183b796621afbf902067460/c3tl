from typing import TypeVar
from c3tl.interfaces.handlers.account_balances.interface import iAccountBalancesHandler


AccountBalancesHandler = TypeVar('AccountBalancesHandler', bound=iAccountBalancesHandler)
