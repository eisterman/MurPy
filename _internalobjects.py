from abc import ABC


class MemObj(ABC):  # Oggetto rappresentante una cella di memoria
    pass


class StackObj(MemObj):  # Oggetto rappresentate variabile statica in Stack
    def __init__(self, value, byte=1):
        self._value = value
        self._byte = byte
        # TODO: Error handling
    # TODO: Getter


class RegObj(MemObj):  # Oggetto rappresentante i registri temporanei
    pass  # TODO: Mi serve?


class HeapOnbj(MemObj):  # Oggetto rappresentante variabile dinamica in Heap
    pass


class RegistryManager:
    def __init__(self, registry):
        self._SIZE = registry
        self._registry = [RegObj()]*self._SIZE

    def __getitem__(self, item):
        return self._registry[item]
