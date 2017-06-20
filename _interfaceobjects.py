from abc import ABC,abstractmethod

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