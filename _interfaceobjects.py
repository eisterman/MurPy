from abc import ABC
from _operations import NewStaticOp, ChangeStaticValueOp, AdditionOp, RegToStackOp, NestedOp


# Nuovi Metodi di Interfaccia
# TODO: Porting in funzione semplice con buffer esterno ç_ç fai leva su protezione modulo
class InterfaceObj(ABC):
    # C'è da overloaddare __init__ per creare InterfaceObj
    buffer = []

    @classmethod
    def GetBuffer(cls):
        tmp = cls.buffer
        cls.buffer = []
        return tmp


class VAR(InterfaceObj):
    def __init__(self, name, value):  # TODO: Typecoding
        # PER ORA SOLO VALORI NUMERICI PURI
        # TODO: Controllo per i Typecode
        op = NewStaticOp(name, value)
        self.buffer.append(op)


class SET(InterfaceObj):
    def __init__(self, name, value):
        if isinstance(value, NestedInterfaceObj):  # TODO: Potrei usare una NestedInterfaceObj
            oplist = [value.getOp(), RegToStackOp(name)]
            op = NestedOp(oplist)
            self.buffer.append(op)
        else:
            op = ChangeStaticValueOp(name, value)
            self.buffer.append(op)


class NestedInterfaceObj(ABC):
    def __init__(self):
        self._OPERATION = None

    def getOp(self):
        return self._OPERATION


class ADD(InterfaceObj, NestedInterfaceObj):
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = AdditionOp(name1, name2)
