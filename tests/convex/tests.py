import unittest
from concurrent.futures import Future

import builtins

from overviews.protocols.convex.overview import (
    ConvexStakingPoolOverview, ConvexStakingPoolAllocationOverview, ConvexStakingPoolIncentiveOverview
)
from overviews.abstracts.fabric import overviewAbstractFabric

from providers.abstracts.fabric import providerAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


class TestConvexStakingPoolOverview(unittest.TestCase):

    _address = '0x22eE18aca7F3Ee920D01F25dA85840D12d98E8Ca'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='staking-pool-overview',
        productKey='convex') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, ConvexStakingPoolOverview)

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


class TestConvexStakingPoolAllocationOverview(unittest.TestCase):

    _address = '0xB900EF131301B307dB5eFcbed9DBb50A3e209B2e'
    _wallet = '0xcb05e41aE2F23A7356e1Cc0eD7db2cd2dC0f9d22'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='staking-pool-allocation-overview',
        productKey='convex') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, ConvexStakingPoolAllocationOverview)

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

            self.assertIsInstance(aOverview['symbol'], str)
            self.assertIsInstance(aOverview['amount'], (int, float))
            self.assertIsInstance(aOverview['price'], (int, float))
        builtins.print('\n', overview)


class TestConvexStakingPoolIncentiveOverview(unittest.TestCase):

    _address = '0xB900EF131301B307dB5eFcbed9DBb50A3e209B2e'
    _wallet = '0xcb05e41aE2F23A7356e1Cc0eD7db2cd2dC0f9d22'

    _provider = BridgeConfigurator(
        abstractFabric=providerAbstractFabric,
        fabricKey='http',
        productKey='eth') \
        .produceProduct()

    _instance = BridgeConfigurator(
        abstractFabric=overviewAbstractFabric,
        fabricKey='staking-pool-incentive-overview',
        productKey='convex') \
        .produceProduct()() \
        .setAddress(address=_address) \
        .setProvider(provider=_provider) \
        .setTrader(trader=headTrader) \
        .create()

    def testInstance(self):
        self.assertIsInstance(self._instance, ConvexStakingPoolIncentiveOverview)

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

            self.assertIsInstance(aOverview['symbol'], str)
            self.assertIsInstance(aOverview['amount'], (int, float))
            self.assertIsInstance(aOverview['price'], (int, float))
        builtins.print('\n', overview)
