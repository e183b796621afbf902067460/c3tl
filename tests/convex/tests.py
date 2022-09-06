from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


provider = BridgeConfigurator(
    abstractFabric=providerAbstractFabric,
    fabricKey='http',
    productKey='eth')\
    .produceProduct()

overview = BridgeConfigurator(
    abstractFabric=overviewAbstractFabric,
    fabricKey='staking-pool-overview',
    productKey='convex')\
    .produceProduct()()\
    .setAddress(address='0x22eE18aca7F3Ee920D01F25dA85840D12d98E8Ca')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overview.getOverview()
result = future.result()

assert isinstance(result[0]['symbol'], str)
assert isinstance(result[0]['reserve'], (int, float))
assert isinstance(result[0]['price'], (int, float))
