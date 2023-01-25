from typing import Generic

from c3tl.interfaces.fabric.interface import iFabric
from c3tl.typings.handlers.account_liquidations.typing import AccountLiquidationsHandler

from c3tl.handlers.account_limit_orders.binance.handlers import BinanceUSDTmAccountLimitOrdersHandler


class AccountLimitOrdersFabric(iFabric):

    def add_handler(self, exchange: str, handler: Generic[AccountLiquidationsHandler]) -> None:
        if not self._handlers.get(exchange):
            self._handlers[exchange] = handler

    def get_handler(self, exchange: str) -> Generic[AccountLiquidationsHandler]:
        handler = self._handlers.get(exchange)
        if not handler:
            raise ValueError(f'Set Account Limit Orders overview handler for {exchange}')
        return handler


accountLimitOrdersFabric = AccountLimitOrdersFabric()

accountLimitOrdersFabric.add_handler(exchange='binance_usdt_m', handler=BinanceUSDTmAccountLimitOrdersHandler)
