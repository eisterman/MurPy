from . import OperatorOperation
# TODO: Documentazione


class AdditionOp(OperatorOperation):
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


class SubtractionOp(OperatorOperation):
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


class MultiplicationOp(OperatorOperation):
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
        # CLEANUP
        clrcode, ptr = env.ClearRegList(R1, (R1, R3, R4))
        code += clrcode
        # code += "[-]" + env.MoveP(R1, R3) + "[-]" + env.MoveP(R3, R4) + "[-]"
        return code, ptr
