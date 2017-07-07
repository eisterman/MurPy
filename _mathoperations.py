from abc import abstractmethod
from collections import OrderedDict
from _operations import Operation, NestedOperation
# TODO: Documentazione


class MathOp(Operation, NestedOperation):
    def __init__(self, name1, name2, nreg, reservebits, exitreg):
        super().__init__()
        self._name1 = name1
        self._name2 = name2
        self._nreg = nreg  # Numero di registri
        self._exitreg = int(exitreg)  # Registro d'uscita (numerazione interna 0,1,2,...)
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
        self._OREGKEY = tuple(choosedreg.keys())[self._exitreg]

    @abstractmethod
    def GetCode(self, env, p):
        pass


class AdditionOp(MathOp):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 2, [True, False], 0)

    def GetCode(self, env, p):
        # TODO: Cominciare a utilizzare i parametri di compilazione
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1, R2 = env.getRegPosition(self._choosedreg.keys())
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
        super().__init__(name1, name2, 2, [True, False], 0)

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1, R2 = env.getRegPosition(self._choosedreg.keys())
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


class MultiplicationOp(MathOp):
    # TODO: Algoritmo speciale per i negativi (parametri di precompilazione per diverse BFVM)
    def __init__(self, name1, name2):
        # Prendo 4 registri per avere una pesante ottimizzazione per il tapeshift.
        super().__init__(name1, name2, 4, [False, True, False, False], 1)

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1, R2, R3, R4 = env.getRegPosition(self._choosedreg.keys())
        code += env.MoveP(p, A)
        # A --> R1, R2
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+" + env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        # R2 -> A
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        code += env.MoveP(R2, B)
        # B -> R3, R4
        code += "[-" + env.MoveP(B, R3) + "+" + env.MoveP(R3, R4) + "+" + env.MoveP(R4, B) + "]"
        code += env.MoveP(B, R3)
        # R3 -> B
        code += "[-" + env.MoveP(R3, B) + "+" + env.MoveP(B, R3) + "]"
        code += env.MoveP(R3, R1)
        # Loop Principale della Moltiplicazione (per ogni R1...)
        code += "[-" + env.MoveP(R1, R4)
        # Loop interno (R4 -> R3, R2
        code += "[-" + env.MoveP(R4, R3) + "+" + env.MoveP(R3, R2) + "+" + env.MoveP(R2, R4) + "]"
        code += env.MoveP(R4, R3)
        # R3 -> R4
        code += "[-" + env.MoveP(R3, R4) + "+" + env.MoveP(R4, R3) + "]"
        # Qui madonne!!!!!!
        code += env.MoveP(R3, R1)
        # Fine Loop interno
        code += "]"
        return code, R1
