import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.ellipsis.overview import EllipsisLiquidityPoolOverview
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestEllipsisLiquidityPoolOverview(unittest.TestCase):

    _address = '0x160CAed03795365F3A589f10C379FfA7d75d4E76'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='liquidity-pool-overview',
        productKey='ellipsis') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, EllipsisLiquidityPoolOverview)

    def testProvider(self):
        self.assertEqual(self._instance.provider, self._provider)

    def testAddress(self):
        self.assertEqual(self._instance.address, self._address)

    def testHead(self):
        self.assertEqual(self._instance.trader, headTrader)

    def test_getOverview(self):
        future = self._instance.getOverview()
        self.assertIsInstance(future, Future)

        overview = future.result()
        self.assertIsInstance(overview, list)

        for aOverview in overview:
            self.assertIsInstance(aOverview, dict)

            self.assertIsInstance(aOverview['symbol'], str)
            self.assertIsInstance(aOverview['reserve'], (int, float))
            self.assertIsInstance(aOverview['price'], (int, float))
        builtins.print('\n', overview)
