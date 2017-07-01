from abc import ABC, abstractmethod
from _internalobjects import StackObj
from collections import OrderedDict


class Operation(ABC):
    @abstractmethod
    def PreCompile(self, env):  # TODO: Decidere cosa cazzo deve ritornare il precompile
        pass

    @abstractmethod
    def GetCode(self, env, p):  # TODO: Argomenti speciali per GetCode, magari usando un item EnvState (?)
        return ""


class NestedOperation(ABC):
    def __init__(self):
        self._IREGKEY = None
        self._OREGKEY = None

    def InputRegKey(self, key):
        self._IREGKEY = key

    def OutputRegKey(self):
        return self._OREGKEY


# TODO: creare un sistema per la memorizzazione tipizzata
class NewStaticOp(Operation):
    def __init__(self, name, value):
        super().__init__()
        self._name = name
        self._value = value

    def PreCompile(self, env):
        if self._name in env.StackObject.keys():
            raise Exception("Duplicated Creation!")
        else:
            env.StackObject[self._name] = StackObj(self._value)

    def GetCode(self, env, p):
        # CASO SPECIALE UN BYTE:
        # TODO: Estensione a multipli Byte
        code = ""
        target = int(list(env.StackObject).index(self._name))
        code += env.MoveP(p, target)
        code += "+" * self._value
        return code, target  # Tuple


class ChangeStaticValueOp(Operation):
    def __init__(self, name, value):
        super().__init__()
        # TODO: Assert the world
        self._name = name  # Id Bersaglio
        self._value = value  # Valore da ficcare nel Berdaglio

    def PreCompile(self, env):
        if self._name not in env.StackObject:  # TODO: Heap support
            raise Exception("Variabile non definita")

    def GetCode(self, env, p):
        code = ""
        target = int(list(env.StackObject).index(self._name))
        env.StackObject[self._name] = StackObj(self._value)  # Per tenere traccia
        if p > target:
            code += "<" * (p - target)
        else:
            code += ">" * (target - p)
        targetval = self._value
        code += '[-]'  # Azzeramento variabile
        code += "+" * targetval
        return code, target


class AdditionOp(Operation, NestedOperation):
    def __init__(self, name1, name2):
        super().__init__()
        self._name1 = name1
        self._name2 = name2
        self._choosedreg = OrderedDict()

    def PreCompile(self, env):  # TODO: Somma Nestata
        if self._name1 not in env.StackObject:
            raise Exception("Variabile non definita")
        if self._name2 not in env.StackObject:
            raise Exception("Variabile non definita")
        # Registry
        choosedreg = self._choosedreg
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(choosedreg) < 2:
                choosedreg[regKey] = regObj
            elif len(choosedreg) == 2:
                break
        while len(choosedreg) < 2:
            regkey, regobj = env.RequestRegistry()
            choosedreg[regkey] = regobj
        vals = list(choosedreg.values())
        vals[0].ReserveBit = True
        vals[1].ReserveBit = False
        self._OREGKEY = list(choosedreg.keys())[0]

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1 = env.getRegPosition(tuple(self._choosedreg.keys())[0])
        R2 = env.getRegPosition(tuple(self._choosedreg.keys())[1])
        code += env.MoveP(p, A)
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        code += env.MoveP(R2, B)
        code += "[-" + env.MoveP(B, R1) + "+" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, B) + "]"
        code += env.MoveP(B, R2)
        code += "[-" + env.MoveP(R2, B) + "+" + env.MoveP(B, R2) + "]"
        code += env.MoveP(R2, R1)
        return code, R1


class RegToStackOp(Operation, NestedOperation):  # PROTOCOLLO NESTEDOP
    def __init__(self, stackname):
        super().__init__()
        self._stackname = stackname

    def PreCompile(self, env):
        if self._stackname not in env.StackObject:  # TODO: Heap support & Assert the World
            raise Exception("Variabile non definita")
        env.RegistryColl[self._IREGKEY].ReserveBit = False

    def GetCode(self, env, p):
        code = ""
        start = env.getRegPosition(self._IREGKEY)
        target = int(list(env.StackObject).index(self._stackname))
        code += env.MoveP(p, target)
        code += "[-]"
        code += env.MoveP(target, start)
        code += "[-" + env.MoveP(start, target) + "+" + env.MoveP(target, start) + "]"
        return code, start


class NestedOp(Operation):  # Risolutore e contenitore di operazioni multiple (per ora protocollo RegKey)
    def __init__(self, oplist):
        super().__init__()
        self._oplist = oplist

    def PreCompile(self, env):
        regbuffer = None
        for op in self._oplist:
            op.InputRegKey(regbuffer)
            op.PreCompile(env)
            regbuffer = op.OutputRegKey()

    def GetCode(self, env, p):
        code = ""
        pointer = int(p)
        for op in self._oplist:
            newcode, newpointer = op.GetCode(env, pointer)
            code += newcode
            pointer = newpointer
        return code, pointer
