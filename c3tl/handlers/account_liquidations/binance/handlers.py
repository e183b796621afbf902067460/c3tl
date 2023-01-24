from c3tl.interfaces.handlers.account_liquidations.interface import iAccountLiquidationsHandler

from c3f1nance.binance.USDTm import BinanceUSDTmExchange
from trad3er.typings.trader.typing import Trad3r

import time
import requests as r


class BinanceUSDTmAccountLiquidationsHandler(BinanceUSDTmExchange, iAccountLiquidationsHandler):

    def __init__(self, trader: Trad3r, *args, **kwargs) -> None:
        BinanceUSDTmExchange.__init__(self, *args, **kwargs)
        iAccountLiquidationsHandler.__init__(self, trader=trader)

    def get_overview(
            self,
            ticker: str,
            *args, **kwargs
    ):
        overviews: list = list()
        position_risk = self.positionRisk(symbol=ticker, timestamp=int(time.time() * 1000))
        if not self._validate_response(position_risk):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        position_risk = position_risk.json()
        for position in position_risk:
            overviews.append(
                {
                    'pit_amt': float(position['positionAmt']),
                    'pit_entry_price': float(position['entryPrice']),
                    'pit_liquidation_price': float(position['liquidationPrice']),
                    'pit_price': self.trader.get_price(first=ticker[:-4], source='binance_usdt_m'),
                    'pit_side': position['positionSide'],
                    'pit_leverage': float(position['leverage']),
                    'pit_un_pnl': float(position['unRealizedProfit'])
                }
            )
        return overviews
