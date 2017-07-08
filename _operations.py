from abc import ABC, abstractmethod
from _internalobjects import StackObj
# TODO: Documentazione


class Operation(ABC):
    @abstractmethod
    def PreCompile(self, env):  # TODO: Decidere cosa cazzo deve ritornare il precompile
        pass

    @abstractmethod
    def GetCode(self, env, p):  # TODO: Argomenti speciali per GetCode, magari usando un item EnvState (?)
        return ""


# TODO: Renderlo figlio di Operation con un unico INIT (?)
class NestedOperation(ABC):
    def __init__(self):
        self._IREGKEY = None
        self._OREGKEY = None

    def InputRegKey(self, key):
        self._IREGKEY = key

    def OutputRegKey(self):
        return self._OREGKEY


# TODO: creare un sistema per la memorizzazione tipizzata
class NewStaticOp(Operation, NestedOperation):
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
