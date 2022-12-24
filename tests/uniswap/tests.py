import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.uniswap.overview import UniSwapV2DEXPoolOverview, UniSwapV2DEXPoolAllocationOverview
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestUniSwapV2DEXPoolOverview(unittest.TestCase):

    _address = '0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='dex-pool-overview',
        productKey='uniswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, UniSwapV2DEXPoolOverview)

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

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_reserve'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
        builtins.print('\n', overview)


class TestUniSwapV2DEXPoolAllocationOverview(unittest.TestCase):

    _address = '0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc'
    _wallet = '0xeC08867a12546ccf53b32efB8C23bb26bE0C04f1'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='dex-pool-allocation-overview',
        productKey='uniswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, UniSwapV2DEXPoolAllocationOverview)

    def testProvider(self):
        self.assertEqual(self._instance.provider, self._provider)

    def testAddress(self):
        self.assertEqual(self._instance.address, self._address)

    def testHead(self):
        self.assertEqual(self._instance.trader, headTrader)

    def test_getOverview(self):
        future = self._instance.getOverview(address=self._wallet)
        self.assertIsInstance(future, Future)

        overview = future.result()
        self.assertIsInstance(overview, list)

        for aOverview in overview:
            self.assertIsInstance(aOverview, dict)

            self.assertIsInstance(aOverview['pit_token_symbol'], str)
            self.assertIsInstance(aOverview['pit_token_amount'], (int, float))
            self.assertIsInstance(aOverview['pit_token_price'], (int, float))
        builtins.print('\n', overview)
