from c3tl.interfaces.fabric.interface import iFabric
from c3tl.abstract.fabric import C3AbstractFabric


class C3BridgeConfigurator:

    def __init__(self, abstract: C3AbstractFabric, fabric_name: str, handler_name: str) -> None:
        self._abstract: C3AbstractFabric = abstract
        self._fabric_name: str = fabric_name
        self._handler_name: str = handler_name

    @property
    def abstract(self) -> C3AbstractFabric:
        return self._abstract

    def produce_fabric(self) -> iFabric:
        return self.abstract.get_fabric(self._fabric_name)

    def produce_handler(self):
        return self.produce_fabric().get_handler(self._handler_name)