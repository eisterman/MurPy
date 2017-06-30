from abc import ABC,abstractmethod
from _operations import Operation,NewStaticOp,ChangeStaticValueOp

# Nuovi Metodi di Interfaccia
# TODO: Porting in funzione semplice con buffer esterno ç_ç fai leva su protezione modulo
class InterfaceObj(ABC):
    buffer = []
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Devi passargli tutti i parametri del comando di interfaccia."""
        pass
    @classmethod
    def getBuffer(cls):
        tmp = cls.buffer
        cls.buffer = []
        return tmp


class var(InterfaceObj):
    def __init__(self, name, value, typecode='ub'): #TODO: Typecoding
        # PER ORA SOLO VALORI NUMERICI PURI
        # TODO: Controllo per i Typecode
        op = NewStaticOp(name,value)
        self.buffer.append(op)


class put(InterfaceObj):
    def __init__(self, name, value):
        op = ChangeStaticValueOp(name,value)
        self.buffer.append(op)