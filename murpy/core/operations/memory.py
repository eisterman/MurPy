from . import Operation, ONestedOperation, NestedOperation

from ..objects.memory import RegObj


# TODO: creare un sistema per la memorizzazione tipizzata
class NewStaticOp(Operation, ONestedOperation):
    def __init__(self, name, value):
        super().__init__()
        self._name = name
        self._value = value
        self._stackobj = None

    def PreCompile(self, env):
        self._stackobj = env.RequestStackName(self._name)
        self._OMEMOBJ = self._stackobj

    def GetCode(self, env, p):
        # CASO SPECIALE UN BYTE:
        # TODO: Estensione a multipli Byte
        code = ""
        target = env.getStackPosition(self._stackobj)
        code += env.MoveP(p, target)
        code += "+" * self._value
        return code, target  # Tuple


class ChangeStaticValueOp(Operation):
    def __init__(self, name, value):
        super().__init__()
        # TODO: Assert the world
        self._name = name  # Id Bersaglio
        self._value = value  # Valore da ficcare nel Berdaglio
        self._stackobj = None

    def PreCompile(self, env):
        # TODO: Heap support
        self._stackobj = env.getStackObjByName(self._name)

    def GetCode(self, env, p):
        code = ""
        target = env.getStackPosition(self._stackobj)
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
        self._stackobj = None

    def PreCompile(self, env):
        self._stackobj = env.getStackObjByName(self._stackname)
        if not isinstance(self._IMEMOBJ, RegObj):
            raise Exception("Richiesto RegObj in IMEMOBJ")
        self._IMEMOBJ.ReserveBit = False
        self._OMEMOBJ = self._stackobj

    def GetCode(self, env, p):
        code = ""
        start = env.getRegPosition(self._IMEMOBJ)
        target = env.getStackPosition(self._stackobj)
        code += env.MoveP(p, target)
        code += "[-]"
        code += env.MoveP(target, start)
        code += "[-" + env.MoveP(start, target) + "+" + env.MoveP(target, start) + "]"
        return code, start


class CopyStackToRegOp(Operation, ONestedOperation):  # PROTOCOLLO NESTEDOP
    def __init__(self, stackname):
        super().__init__()
        self._stackname = stackname
        self._targetreg = []
        self._stackobj = None

    def PreCompile(self, env):
        self._stackobj = env.getStackObjByName(self._stackname)
        reservedreg = self._targetreg
        nreg = 2
        for regObj in env.RegistryColl.values():
            if not regObj.ReserveBit and len(reservedreg) < nreg:
                reservedreg.append(regObj)
            elif len(reservedreg) == nreg:
                break
        while len(reservedreg) < nreg:
            regObj = env.RequestRegistry()
            reservedreg.append(regObj)
        # Ref Power
        self._targetreg[0].ReserveBit = True
        self._targetreg[1].ReserveBit = False
        self._OMEMOBJ = reservedreg[0]

    def GetCode(self, env, p):
        code = ""
        A = env.getStackPosition(self._stackobj)
        R1 = env.getRegPosition(self._targetreg[0])
        R2 = env.getRegPosition(self._targetreg[1])
        code += env.MoveP(p, R1)
        code += "[-]"
        code += env.MoveP(R1, A)
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+"
        code += env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        return code, R2
