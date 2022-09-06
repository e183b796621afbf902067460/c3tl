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
    fabricKey='lending-pool-overview',
    productKey='sturdy')\
    .produceProduct()()\
    .setAddress(address='0xA422CA380bd70EeF876292839222159E41AAEe17')\
    .setProvider(provider=provider)\
    .setTrader(trader=headTrader)\
    .create()


assets = overview.getReservesList()


futures = list()
for asset in assets:
    future = overview.getOverview(asset)
    futures.append(future)

for future in futures:
    _ = future.result()
    if _:
        assert isinstance(_[0]['reserve'], (int, float))
        assert isinstance(_[0]['borrow'], (int, float))
        assert isinstance(_[0]['price'], (int, float))
