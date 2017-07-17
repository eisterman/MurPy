from _operations import Operation, NestedOperation
from _internalobjects import StackObj


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


class CopyStackToRegOp(Operation, NestedOperation):  # PROTOCOLLO NESTEDOP
    def __init__(self, stackname):
        super().__init__()
        self._stackname = stackname
        self._targetreg = {}

    def PreCompile(self, env):
        if self._stackname not in env.StackObject:
            raise Exception("Variabile non definita")
        reservedreg = self._targetreg
        nreg = 2
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(reservedreg) < nreg:
                reservedreg[regKey] = regObj
            elif len(reservedreg) == nreg:
                break
        while len(reservedreg) < nreg:
            regKey, regObj = env.RequestRegistry()
            reservedreg[regKey] = regObj
        # Ref Power
        vals = list(reservedreg.values())
        vals[0].ReserveBit = True
        vals[1].ReserveBit = False
        self._OREGKEY = tuple(reservedreg.keys())[0]

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._stackname))
        R1 = env.getRegPosition(list(self._targetreg.keys())[0])
        R2 = env.getRegPosition(list(self._targetreg.keys())[1])
        code += env.MoveP(p, R1)
        code += "[-]"
        code += env.MoveP(R1, A)
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+"
        code += env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        return code, R2
