from abc import abstractmethod
from collections import OrderedDict
from _operations import Operation, NestedOperation
# TODO: Documentazione


class MathOp(Operation, NestedOperation):
    def __init__(self, name1, name2, nreg, reservebits):
        super().__init__()
        self._name1 = name1
        self._name2 = name2
        self._nreg = nreg  # Numero di registri
        self._reservebits = reservebits  # Bit di riserva post operazione
        self._choosedreg = OrderedDict()

    def PreCompile(self, env):  # TODO: Somma Nestata
        if self._name1 not in env.StackObject:
            raise Exception("Variabile non definita")
        if self._name2 not in env.StackObject:
            raise Exception("Variabile non definita")
        # Registry
        choosedreg = self._choosedreg
        nreg = self._nreg
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(choosedreg) < nreg:
                choosedreg[regKey] = regObj
            elif len(choosedreg) == nreg:
                break
        while len(choosedreg) < nreg:
            regkey, regobj = env.RequestRegistry()
            choosedreg[regkey] = regobj
        vals = list(choosedreg.values())
        for i in range(len(vals)):
            vals[i].ReserveBit = self._reservebits[i]
        self._OREGKEY = list(choosedreg.keys())[0]

    @abstractmethod
    def GetCode(self, env, p):
        pass


class AdditionOp(MathOp):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 2, [True, False])

    def GetCode(self, env, p):
        # TODO: Cominciare a utilizzare i parametri di compilazione
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


class SubtractionOp(MathOp):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 2, [True, False])

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
        code += "[-" + env.MoveP(B, R1) + "-" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, B) + "]"
        code += env.MoveP(B, R2)
        code += "[-" + env.MoveP(R2, B) + "+" + env.MoveP(B, R2) + "]"
        code += env.MoveP(R2, R1)
        return code, R1
