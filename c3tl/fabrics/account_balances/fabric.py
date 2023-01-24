from typing import Generic

from c3tl.interfaces.fabric.interface import iFabric
from c3tl.typings.handlers.account_balances.typing import AccountBalancesHandler

from c3tl.handlers.account_balances.binance.handlers import BinanceSpotAccountBalancesHandler, BinanceUSDTmAccountBalancesHandler


class AccountBalancesFabric(iFabric):

    def add_handler(self, exchange: str, handler: Generic[AccountBalancesHandler]) -> None:
        if not self._handlers.get(exchange):
            self._handlers[exchange] = handler

    def get_handler(self, exchange: str) -> Generic[AccountBalancesHandler]:
        handler = self._handlers.get(exchange)
        if not handler:
            raise ValueError(f'Set Account Balances overview handler for {exchange}')
        return handler


accountBalancesFabric = AccountBalancesFabric()

accountBalancesFabric.add_handler(exchange='binance_spot', handler=BinanceSpotAccountBalancesHandler)
accountBalancesFabric.add_handler(exchange='binance_usdt_m', handler=BinanceUSDTmAccountBalancesHandler)
