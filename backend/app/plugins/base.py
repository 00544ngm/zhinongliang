from abc import ABC, abstractmethod


class PluginInterface(ABC):
    name: str = "base_plugin"

    @abstractmethod
    async def initialize(self):
        pass

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass
