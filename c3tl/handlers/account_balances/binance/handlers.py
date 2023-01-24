from c3tl.interfaces.handlers.account_balances.interface import iAccountBalancesHandler

from c3f1nance.binance.Spot import BinanceSpotExchange
from c3f1nance.binance.USDTm import BinanceUSDTmExchange
from trad3er.typings.trader.typing import Trad3r

import time
import requests as r


class BinanceSpotAccountBalancesHandler(BinanceSpotExchange, iAccountBalancesHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceSpotExchange.__init__(self, *args, **kwargs)
        iAccountBalancesHandler.__init__(self, trader=trader)

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        account = account.json()
        for balance in account['balances']:
            if balance['asset'] == ticker:
                overviews.append(
                    {
                        'pit_qty': float(balance['free']) + float(balance['locked']),
                        'pit_price': self.trader.get_price(first=balance['asset'])
                    }
                )
                break
        return overviews


class BinanceUSDTmAccountBalancesHandler(BinanceUSDTmExchange, iAccountBalancesHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceUSDTmExchange.__init__(self, *args, **kwargs)
        iAccountBalancesHandler.__init__(self, trader=trader)

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        account = account.json()

        for asset in account['assets']:
            if asset['asset'] == ticker:
                overviews.append(
                    {
                        'pit_qty': float(asset['marginBalance']),
                        'pit_price': self.trader.get_price(first=asset['asset'])
                    }
                )
                break
        return overviews
