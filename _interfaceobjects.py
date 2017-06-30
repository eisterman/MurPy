from abc import ABC,abstractmethod
from _operations import newOperation

class InterfaceObj(ABC): # Oggetti di interfaccia con l'esterno
    @abstractmethod
    def getValue(self):
        pass
    @abstractmethod
    def getByte(self):
        pass

class Byte(InterfaceObj):
    def __init__(self,value):
        self._val = int(value)
        self._byte = 1
        #TODO: Value Handling
    def getByte(self):
        return self._byte
    def getValue(self):
        return self._val

# Nuovi Metodi di Interfaccia
class newInterfaceObj(ABC):
    buffer = []
    @classmethod
    def getBuffer(cls):
        tmp = cls.buffer
        cls.buffer = []
        return tmp
    @abstractmethod
    def __call__(self, *args, **kwargs):
        """Devi passargli tutti i parametri del comando di interfaccia."""
        pass

class protovar(newInterfaceObj):
    def __call__(self, name, value, typecode='ub'): #TODO: Typecoding
        # PER ORA SOLO VALORI NUMERICI PURI
        # TODO: Controllo per i Typecode
        pass
