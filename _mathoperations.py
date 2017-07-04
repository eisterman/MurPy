from abc import abstractmethod
from collections import OrderedDict
from _operations import Operation, NestedOperation
# TODO: Documentazione


class MathOp(Operation, NestedOperation):
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

    @abstractmethod
    def GetCode(self, env, p):
        pass


class AdditionOp(MathOp):
    def __init__(self, name1, name2):
        super().__init__(name1, name2)

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1 = env.getRegPosition(tuple(self._choosedreg.keys())[0])
        R2 = env.getRegPosition(tuple(self._choosedreg.keys())[1])
        code += env.MoveP(p, A)
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        # TODO: MISSING OPTIMIZATION
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        code += env.MoveP(R2, B)
        code += "[-" + env.MoveP(B, R1) + "+" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, B) + "]"
        code += env.MoveP(B, R2)
        code += "[-" + env.MoveP(R2, B) + "+" + env.MoveP(B, R2) + "]"
        code += env.MoveP(R2, R1)
        return code, R1


class SubtractionOp(MathOp):
    def __init__(self, name1, name2):
        super().__init__(name1, name2)

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
