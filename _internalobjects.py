from abc import ABC


class MemObj(ABC):  # Oggetto rappresentante una cella di memoria
    """
    Abstract Base Class used as Interface for all the object
    reppresenting a Memory Object.
    """
    pass


class StackObj(MemObj):  # Oggetto rappresentate variabile statica in Stack
    """
    Object used to reppresent a Object in the Stack of the
    machine. This will contain all the info about the
    contained data.
    """
    def __init__(self, value, byte=1):
        """
        Build a new StackObj instance.
        :param value: Value of the Stack Object. Unused at now.
        :param byte: Number of bytes allocated from the object.
        """
        assert byte >= 1
        self._value = int(value)
        self._byte = int(byte)
    # TODO: Getter (?)


class RegObj(MemObj):  # Oggetto rappresentante i registri temporanei
    """
    Object used to reppresent a Registry in the Registry Zone of
    the machine stack. This object will contain all the info about
    the registry status and data.
    """
    def __init__(self, value=0, reserved=True, byte=1):
        """
        Build a new RegObj instance.
        :param value: Value of the Registry. Unused at now.
        :param reserved: Status of the Registry. Is at now the registry used from one operation?
        :param byte: Number of bytes allocated from the object.
        """
        assert byte >= 1
        self._value = int(value)
        self._reserved = bool(reserved)
        self._byte = int(byte)

    @property
    def ReserveBit(self):
        """Get if the registry appear as used from some operation."""
        return self._reserved

    @ReserveBit.setter
    def ReserveBit(self, other):
        """Set if the registry appear as used from some operation."""
        self._reserved = bool(other)


class HeapOnbj(MemObj):  # Oggetto rappresentante variabile dinamica in Heap
    """Unused Object. Only PlaceHolder."""
    pass
