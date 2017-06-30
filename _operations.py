from abc import ABC, abstractmethod
from _internalobjects import StackObj


class Operation(ABC):
    @abstractmethod
    def PreCompile(self, env):  # TODO: Decidere cosa cazzo deve ritornare il precompile
        pass

    @abstractmethod
    def GetCode(self, env, p):  # TODO: Argomenti speciali per GetCode, magari usando un item EnvState (?)
        return ""


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
        if p > target:
            code += "<" * (p - target)
        else:
            code += ">" * (target - p)
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
