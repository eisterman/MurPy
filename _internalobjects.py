from abc import ABC,abstractmethod

class MemObj(ABC): # Oggetto rappresentante una cella di memoria
    pass

class StackObj(MemObj): # Oggetto rappresentate variabile statica in Stack
    def __init__(self,value,byte):
        self._value = value
        self._byte = byte
        #TODO: Error handling
    #TODO: Getter

class RegObj(MemObj): # Oggetto rappresentante i registri temporanei
    pass #TODO: Preparare l'infrastruttura per la memorizzazione delle registryOperation

class HeapOnbj(MemObj): # Oggetto rappresentante variabile dinamica in Heap
    pass

class RegistryManager:
    def __init__(self,Registry):
        self._SIZE = Registry
        self._registry = [RegObj()]*self._SIZE
    def __getitem__(self, item):
        return self._registry[item]

