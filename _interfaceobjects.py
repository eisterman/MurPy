from abc import ABC
from _operations import NewStaticOp, ChangeStaticValueOp


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


class var(InterfaceObj):
    def __init__(self, name, value):  # TODO: Typecoding
        # PER ORA SOLO VALORI NUMERICI PURI
        # TODO: Controllo per i Typecode
        op = NewStaticOp(name, value)
        self.buffer.append(op)


class put(InterfaceObj):
    def __init__(self, name, value):
        op = ChangeStaticValueOp(name, value)
        self.buffer.append(op)
