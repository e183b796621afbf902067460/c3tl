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
    productKey='uniswap')\
    .produceProduct()()\
    .setAddress(address='0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


future = overviewContract.getOverview()
overview = future.result()

for aOverview in overview:
    assert isinstance(aOverview['symbol'], str)
    assert isinstance(aOverview['reserve'], (int, float))
    assert isinstance(aOverview['price'], (int, float))
