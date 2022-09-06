from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader
from head.bridge.configurator import BridgeConfigurator


provider = BridgeConfigurator(
    abstractFabric=providerAbstractFabric,
    fabricKey='http',
    productKey='eth')\
    .produceProduct()

overviewContract = BridgeConfigurator(
    abstractFabric=overviewAbstractFabric,
    fabricKey='liquidity-pool-overview',
    productKey='curve')\
    .produceProduct()()\
    .setAddress(address='0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overviewContract.getOverview()
overview = future.result()

for aOverview in overview:
    assert isinstance(aOverview['symbol'], str)
    assert isinstance(aOverview['reserve'], (int, float))
    assert isinstance(aOverview['price'], (int, float))
