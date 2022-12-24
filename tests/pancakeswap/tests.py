import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.pancakeswap.overview import (
    PancakeSwapDEXPoolOverview, PancakeSwapFarmingPoolAllocationOverview, PancakeSwapFarmingPoolOverview,
    PancakeSwapFarmingPoolIncentiveOverview
)
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestPancakeSwapDEXPoolOverview(unittest.TestCase):

    _address = '0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='dex-pool-overview',
        productKey='pancakeswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, PancakeSwapDEXPoolOverview)

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


class TestPancakeSwapFarmingPoolOverview(unittest.TestCase):

    _address = '0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='farming-pool-overview',
        productKey='pancakeswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, PancakeSwapFarmingPoolOverview)

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


class TestPancakeSwapFarmingPoolAllocationOverview(unittest.TestCase):

    _address = '0x2354ef4DF11afacb85a5C7f98B624072ECcddbB1'
    _wallet = '0xD183F2BBF8b28d9fec8367cb06FE72B88778C86B'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='farming-pool-allocation-overview',
        productKey='pancakeswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, PancakeSwapFarmingPoolAllocationOverview)

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


class TestPancakeSwapFarmingPoolIncentiveOverview(unittest.TestCase):

    _address = '0x2354ef4DF11afacb85a5C7f98B624072ECcddbB1'
    _wallet = '0xD183F2BBF8b28d9fec8367cb06FE72B88778C86B'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='bsc') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='farming-pool-incentive-overview',
        productKey='pancakeswap') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, PancakeSwapFarmingPoolIncentiveOverview)

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
