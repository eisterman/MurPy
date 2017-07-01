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
    def __init__(self, value=0, reserved=True, byte=1):
        self._value = value
        self._reserved = reserved
        self._byte = byte

    @property
    def ReserveBit(self):
        return self._reserved

    @ReserveBit.setter
    def ReserveBit(self, other):
        self._reserved = bool(other)


class HeapOnbj(MemObj):  # Oggetto rappresentante variabile dinamica in Heap
    pass
