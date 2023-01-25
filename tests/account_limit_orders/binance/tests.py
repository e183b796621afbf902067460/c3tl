import unittest

import builtins
from datetime import datetime, timezone, timedelta

from c3tl.handlers.account_limit_orders.binance.handlers import BinanceUSDTmAccountLimitOrdersHandler
from c3tl.abstract.fabric import c3Abstract
from c3tl.bridge.configurator import C3BridgeConfigurator

from trad3er.root.composite.trader import rootTrad3r


class TestBinanceUSDTmAccountLimitOrdersHandler(unittest.TestCase):

    api = ''
    secret = ''

    product = C3BridgeConfigurator(
        abstract=c3Abstract,
        fabric_name='account_limit_orders',
        handler_name='binance_usdt_m'
    ).produce_handler()
    handler = product(
        api=api,
        secret=secret,
        trader=rootTrad3r
    )

    def testInstance(self):
        self.assertIsInstance(self.handler, BinanceUSDTmAccountLimitOrdersHandler)

    def test_get_overview(self):

        overview = self.handler.get_overview(
            ticker='ETHUSDT',
        )
        builtins.print('\n', overview)