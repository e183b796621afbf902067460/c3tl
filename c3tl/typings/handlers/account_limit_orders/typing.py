from typing import TypeVar
from c3tl.interfaces.handlers.account_limit_orders.interface import iAccountLimitOrdersHandler


AccountLimitOrdersHandler = TypeVar('AccountLimitOrdersHandler', bound=iAccountLimitOrdersHandler)
