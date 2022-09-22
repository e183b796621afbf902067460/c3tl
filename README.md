# DeFi Overviews Fabric

Depends on: [defi-head-core](https://github.com/e183b796621afbf902067460/defi-head-core), [defi-providers-fabric](https://github.com/e183b796621afbf902067460/defi-providers-fabric), [defi-contracts-evm](https://github.com/e183b796621afbf902067460/defi-contracts-evm) and for tests will be needed [hybrid-traders-composite](https://github.com/e183b796621afbf902067460/hybrid-traders-composite).

---
The Overview object is a complex class that helps to get the necessary data from a smart contract. Different Overviews return different data. Based on input arguments an [`OverviewAbstractFabric`](https://github.com/e183b796621afbf902067460/defi-overviews-fabric/blob/master/overviews/abstracts/fabric.py) return [`IConcreteFabric`](https://github.com/e183b796621afbf902067460/defi-head-core/blob/master/head/interfaces/fabrics/interface.py) object such as: [*LiquidityPoolOverviewFabric*](https://github.com/e183b796621afbf902067460/defi-overviews-fabric/blob/master/overviews/fabrics/liquidityPool/fabric.py), [*StakingPoolOverviewFabric*](https://github.com/e183b796621afbf902067460/defi-overviews-fabric/blob/master/overviews/fabrics/stakingPool/fabric.py) or  [*LendingPoolOverviewFabric*](https://github.com/e183b796621afbf902067460/defi-overviews-fabric/blob/master/overviews/fabrics/lendingPool/fabric.py).
`IConcreteFabric` (Liquidity, Staking or Lending) can produce needed [`IInstrumentOverview Class`](https://github.com/e183b796621afbf902067460/defi-head-core/blob/master/head/interfaces/overview/builder.py) for different purposes.

# Usage
For example, to get [`CurveLiquidityPoolOverview`](https://github.com/e183b796621afbf902067460/defi-overviews-fabric/blob/master/overviews/protocols/curve/overview.py) need to call [`BridgeConfigurator`](https://github.com/e183b796621afbf902067460/defi-head-core/blob/master/head/bridge/configurator.py) and pass to it constructor next arguments and then call `produceProduct()` method:
```
from head.bridge.configurator import BridgeConfigurator
from overviews.abstracts.fabric import overviewAbstractFabric   


concreteFabricKey = 'liquidity-pool-overview'
concreteProductKey = 'curve'

overview = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey=concreteFabricKey,
            productKey=concreteProductKey) \
            .produceProduct()
```

Current overview object is `CurveLiquidityPoolOverview`. After it's production need to set certain __properties__ to call `getOverview()` method correctly. Let's see how it works in synergy:
```
from head.bridge.configurator import BridgeConfigurator

from providers.abstracts.fabric import providerAbstractFabric
from overviews.abstracts.fabric import overviewAbstractFabric
from traders.head.trader import headTrader


_address = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'


_provider = BridgeConfigurator(
            abstractFabric=providerAbstractFabric,
            fabricKey='http',
            productKey='eth') \
            .produceProduct()
            
instance = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey='liquidity-pool-overview',
            productKey='curve') \
            .produceProduct()() \
            .setAddress(address=_address) \
            .setProvider(provider=_provider) \
            .setTrader(trader=headTrader) \
            .create()
```
After call `instance.getOverview()` it'll return a __Future__ object because it's a [@threadmethod](https://github.com/e183b796621afbf902067460/defi-head-core/blob/master/head/decorators/threadmethod.py), so if returned value is needed just call `instance.getOverview().result()`, but only in test environment.

All fabrics and products keys can be viewed in the right factories.
